import pytest

from rest_framework import status
from methodist.tests.api.urls import SubjectUrl
from methodist.api.views import SubjectApi
from methodist.tests.api.schemas.subject import SubjectsSchema, SubjectDetailSchema
from methodist.models import Subject


pytestmark = [pytest.mark.django_db]


def test_list_subjects(methodist_api, subjects):
    response = methodist_api.get(
        path=SubjectUrl.SUBJECT_BASE.value,
        view=SubjectApi,
        view_kwargs={"get": "list"},
        status=status.HTTP_200_OK
    )

    assert SubjectsSchema(**response.data['results'][0])


def test_detail_subjects(methodist_api, subjects):
    response = methodist_api.get(
        path=SubjectUrl.SUBJECT_BASE.value,
        view=SubjectApi,
        view_kwargs={"get": "retrieve"},
        status=status.HTTP_200_OK,
        detail_args={"pk": 1}
    )

    assert SubjectDetailSchema(**response.data)


def test_create_subjects(methodist_api, data):
    assert not Subject.objects.exists()
    response = methodist_api.post(
        path=SubjectUrl.SUBJECT_BASE.value,
        data=data,
        view=SubjectApi,
        status=status.HTTP_201_CREATED,
        view_kwargs={"post": "create"}
    )

    assert Subject.objects.exists()
    assert SubjectsSchema(**response.data)


def test_update_subject(methodist_api, subjects, data):
    subject = Subject.objects.first()

    assert subject.name_subject != data['name_subject']

    methodist_api.put(
        path=SubjectUrl.SUBJECT_BASE.value,
        data=data,
        view=SubjectApi,
        view_kwargs={"put": "update"},
        status=status.HTTP_200_OK,
        detail_args={"pk": subjects.id}
    )
    subject.refresh_from_db()
    name_subject = subject.name_subject.split(' (')

    assert len(name_subject) == 2
    assert name_subject[0] == data['name_subject']
