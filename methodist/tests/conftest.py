import pytest

from mixer.backend.django import mixer
from datetime import date

from GradeBookGC_BACKEND.request_factory import APITestRequestFactory
from methodist.constants import CURRENT_YEAR, STUDENT_GROUP_ID, DEPARTMENT_ID_TEST
from methodist.models.choices import FormEducationChoice


pytestmark = [pytest.mark.django_db]


EXAMPLE_GROUPS = [
    'КН-41',
    'О-12',
    'КН-31',
    'О-22',
    'Й-23'
]


@pytest.fixture
def methodist_api():
    return APITestRequestFactory(perm='Методист')


@pytest.fixture
def not_methodist_api():
    return APITestRequestFactory(perm='Студент')


@pytest.fixture
def groups():
    return [{"name": group, "id": index} for index, group in enumerate(EXAMPLE_GROUPS, 1)]


@pytest.fixture
def current_year():
    return CURRENT_YEAR


@pytest.fixture
def year_entry(current_year):
    return [
        date(current_year - 1, 8, 15),
        date(current_year, 8, 15),
        date(current_year - 2, 8, 15),
        date(current_year - 1, 8, 15),
        date(current_year - 5, 8, 15),
    ]


@pytest.fixture
def departments():
    return [
        DEPARTMENT_ID_TEST,
        DEPARTMENT_ID_TEST,
        DEPARTMENT_ID_TEST,
        2,
        DEPARTMENT_ID_TEST
    ]


@pytest.fixture
def users(departments):
    return mixer.cycle(5).blend(
        'methodist.CustomUser',
        group_id=STUDENT_GROUP_ID,
        group__name="Студент",
        department_id=(department for department in departments),
    )


@pytest.fixture
def students(groups, year_entry, users):
    return mixer.cycle(5).blend(
        'methodist.Student',
        group__name=(group['name'] for group in groups),
        group_id=(group['id'] for group in groups),
        user=(user for user in users),
        update_at=(_ for _ in year_entry),
        year_entry=(_ for _ in year_entry),
        form_education=FormEducationChoice.CONTRACT.value
    )

