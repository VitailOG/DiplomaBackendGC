import pytest

from mixer.backend.django import mixer

from methodist.models import ControlChoice


@pytest.fixture
def educational_program():
    return mixer.blend('methodist.EducationalProgram')


@pytest.fixture
def group():
    return mixer.blend('methodist.Group')


@pytest.fixture
def extra_point(subjects, students):
    return mixer.blend(
        'methodist.ExtraPoints',
        user_id=students[1].id,
        point='0.2',
        semester=subjects.semester
    )


@pytest.fixture(autouse=True)
def subjects(groups):
    return mixer.blend(
        'methodist.Subject',
        name_subject='Mатематика',
        group_id=groups[0]['id']
    )


@pytest.fixture
def ratings(subjects, groups, students):
    return mixer.blend(
        'methodist.Rating',
        user_id=students[1].id,
        semester=subjects.semester,
        rating_5=5,
        subject__form_of_control=ControlChoice.PRACTICE.value,
        is_annual_assessment=True
    )


@pytest.fixture
def data(methodist, group):
    return {
        "name_subject": "new name",
        "group": group.id,
        "teachers": [
            methodist.id
        ],
        "hours": 10,
        "semester": 1,
        "final_semester": 1,
        "form_of_control": "Екзамен",
        "url_on_moodle": "http://192.168.0.103:8000/swagger/",
        "finally_subject": True
    }
