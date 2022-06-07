import pytest

from methodist.services.update_group_students import UpdateGroupStudentService


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def service(students, groups):
    return UpdateGroupStudentService(
            students=students,
            groups=groups
        )


@pytest.mark.parametrize(
    ("method", "name", "result"),
    [
        ("isdigit", "КН-31", "31"),
        ("isdigit", "!#-?", ""),
        ("isdigit", 321321, False),
        ("isalpha", "КН-31", "КН")
    ]
)
def test_symbols_by_methods(service, method, name, result):
    assert service._symbols_by_method(method, name) == result


@pytest.mark.parametrize(
    ("prefix", "num", "result"),
    [
        ("КН", "31", True),
        ("КН", "41", False),
        ("О", "12", True),
        ("Й", "23", False)
    ]
)
def test_is_group(service, prefix, num, result):
    assert service._is_group(prefix=prefix, num=num) is result


@pytest.mark.parametrize(
    ("group", "result"),
    [
        ("КН-41", 1),
        ("О-22", 4)
    ]
)
def test_next_obj(service, group, result):
    assert service._next_obj(group) == result


def test_execute(service, students, current_year):
    assert students[0].group.name == "КН-41"
    assert students[1].group.name == "О-12"
    assert students[2].group.name == "КН-31"
    assert students[4].group.name == "Й-23"
    service()
    assert students[0].group is None
    assert students[1].group.name == "О-12"
    assert students[2].group.name == "КН-41"
    assert students[4].group is None
    assert all(_.update_at.year == current_year for _ in students)


def test_double_call_of_year(service, students):
    assert students[2].group.name == "КН-31"
    service()
    assert students[2].group.name == "КН-41"
    service()
    assert students[2].group.name == "КН-41"
