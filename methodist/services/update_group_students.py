from typing import Literal
from dataclasses import dataclass

from django.utils import timezone

from methodist.models.users import Student
from methodist.constants import CURRENT_YEAR

METHODS = Literal[
    "isalpha",
    "isdigit",
]


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return False
    return inner


@dataclass
class UpdateGroupStudentService:
    """ Сервіс для зміни в студентів групи
        Ф-Ї:
            - Вибирання всі символів(цифри або букви) із рядка
            - Перевірка потрібної групи
            - Пошук id потрібної групи
            - Саме редагування
        Принцип дії:
            - якщо рік вступу або рік останьої спрови редагування
                                                студента дорівнює поточному року, тоді група в нього не міняється
            - якщо рік вступу не дорівнює поточному року і група находиться, тоді замінюється
            - якщо рік вступу не дорівнює поточному року і група не находиться, тоді в полі група проставляється None
        Приклад використання - UpdateGroupStudentService(
                                     groups=list(Group.objects.values("name", "id")),
                                     students=Student.objects.active_students(department=Department.objects.get(id=5))
                                )()
    """
    groups: list[dict[str, str | int]]
    students: Student

    def __post_init__(self):
        self.groups_name = [i.get('name') for i in self.groups]

    def __call__(self):
        return self._change_group()

    @error_handler
    def _symbols_by_method(self, method: METHODS, name: str) -> str | bool:
        return ''.join(filter(getattr(str, method), name))

    @error_handler
    def _is_group(self, prefix: str, num: str) -> bool:
        return any(
                [
                    self._symbols_by_method('isalpha', i) == prefix and
                    int(self._symbols_by_method('isdigit', i)) > int(num)
                    for i in self.groups_name
                ]
            )

    def _next_obj(self, group: str) -> int:
        obj = list(filter(lambda x: x['name'] == group, self.groups))[0]
        return obj.get('id')

    def _change_group(self) -> None:

        for student in self.students:

            group_name = getattr(student.group, 'name', None)
            prefix = self._symbols_by_method('isalpha', group_name)
            num = self._symbols_by_method('isdigit', group_name)

            entry_year = student.year_entry.year
            update_year = getattr(student.update_at, 'year', entry_year)

            if CURRENT_YEAR in (update_year, entry_year):
                continue

            elif self._is_group(prefix=prefix, num=num):
                group = f'{prefix}-{int(num) + 10}'
                student.group_id = self._next_obj(group=group)
                student.update_at = timezone.now().date()

            else:
                student.group = None
                student.update_at = timezone.now().date()

        Student.objects.bulk_update(self.students, fields=['group', 'update_at'])
