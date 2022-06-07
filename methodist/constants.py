from django.utils.timezone import now

from methodist.models.choices import ControlChoice


SEMESTER_FOR_COURSE = {
    '1': [1, 2],
    '2': [3, 4],
    '3': [5, 6],
    '4': [7, 8]
}

CURRENT_YEAR = now().year

STUDENT_GROUP_ID = 4
TEACHER_GROUP_ID = 3

DEPARTMENT_ID_TEST = 1

OTHER_CONTROL = (ControlChoice.PRACTICE.value, ControlChoice.TERM_PAPER.value)
