import pytest

from datetime import date
from rest_framework import status

from methodist.api.views import StudentApi
from methodist.constants import DEPARTMENT_ID_TEST
from methodist.models import Student
from methodist.tests.api.urls import StudentUrl
from methodist.tests.api.schemas.student import StudentListSchema, UserSchema


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def present_student_data(group):
    return {
        "year_entry": "2022-04-03",
        "group": group.id,
        "form_education": "Державна"
    }


def test_student_list_methodist(methodist_api, students):
    response = methodist_api.get(
        path=StudentUrl.STUDENT_BASE.value,
        view=StudentApi,
        view_kwargs={"get": "list"},
        status=status.HTTP_200_OK
    )
    validate_response = StudentListSchema(**response.data['results'][0])

    assert all([_['user']['department'] == DEPARTMENT_ID_TEST for _ in response.data['results']])
    assert validate_response
    assert response.data['count'] == 3


def test_student_list_not_methodist(not_methodist_api, students):
    not_methodist_api.get(
        path=StudentUrl.STUDENT_BASE.value,
        view=StudentApi,
        view_kwargs={"get": "list"},
        status=status.HTTP_403_FORBIDDEN
    )


def test_create_student_methodist(methodist_api, users, present_student_data):
    student = Student.objects.filter(user_id=users[0].id)
    assert not student.exists()

    request = methodist_api.post(
        path=StudentUrl.STUDENT_CREATE.value,
        view=StudentApi,
        view_kwargs={"post": "create_student"},
        data=present_student_data,
        status=status.HTTP_201_CREATED,
        detail_args={"user_id": users[0].id}
    )

    assert student.exists()
    assert request.data['created'] is True


def test_create_student_not_methodist(not_methodist_api, users, present_student_data):
    not_methodist_api.post(
        path=StudentUrl.STUDENT_CREATE.value,
        view=StudentApi,
        view_kwargs={"post": "create_student"},
        data=present_student_data,
        status=status.HTTP_403_FORBIDDEN,
        detail_args={"user_id": users[0].id}
    )


def test_students_without_group(methodist_api, users):
    response = methodist_api.get(
        path=StudentUrl.STUDENT_WITHOUT_GROUP.value,
        view=StudentApi,
        view_kwargs={"get": "get_students_without_group"},
        status=status.HTTP_200_OK
    )

    assert all([_['department'] == DEPARTMENT_ID_TEST for _ in response.data])
    assert len(response.data) == 4
    assert UserSchema(**response.data[0])


def test_update_student(methodist_api, students, group, present_student_data):
    def convert_str_to_date(_date: str) -> date:
        return date(*map(int, _date.split('-')))

    student = students[0]

    assert student.year_entry == convert_str_to_date(_date="2021-08-15")

    response = methodist_api.put(
        path=StudentUrl.STUDENT_BASE.value,
        view=StudentApi,
        data=present_student_data,
        view_kwargs={"put": "update"},
        status=status.HTTP_200_OK,
        detail_args={"pk": student.id}
    )

    student.refresh_from_db()

    assert response.status_code == 200
    assert StudentListSchema(**response.data)
    assert students[0].year_entry == convert_str_to_date(_date=present_student_data['year_entry'])


def test_update_student_(not_methodist_api, students, present_student_data):
    student = students[0]

    not_methodist_api.put(
        path=StudentUrl.STUDENT_BASE.value,
        view=StudentApi,
        data=present_student_data,
        view_kwargs={"put": "update"},
        status=status.HTTP_403_FORBIDDEN,
        detail_args={"pk": student.id}
    )
