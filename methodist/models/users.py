from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.functional import cached_property
from django_lifecycle import (
    LifecycleModel,
    hook,
    BEFORE_UPDATE,
    BEFORE_CREATE
)

from methodist.managers.user import UserManager
from methodist.managers.student import StudentManager
from methodist.models.choices import FormEducationChoice


class CustomUser(LifecycleModel, AbstractUser):
    """ Extend models `User`
    """
    objects = UserManager()

    surname = models.CharField(verbose_name='По батькові', max_length=50)

    group = models.ForeignKey(
        'Permissions',
        on_delete=models.CASCADE,
        verbose_name='Права доступу',
        null=True
    )

    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        verbose_name='Відділ',
        null=True
    )

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    # @hook(AFTER_UPDATE, when='group', was='Студент', is_not='Студент')
    # def remove_student_obj(self):
    #     if hasattr(self, 'student'):
    #         self.student.delete()


class Student(LifecycleModel):
    """ Model for students
    """

    objects = StudentManager()

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student'
    )

    year_entry = models.DateField(verbose_name="Рік вступу")

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name="Група",
        related_name="groups",
        related_query_name="student_group",
        null=True
    )

    educational_program = models.ForeignKey(
        'EducationalProgram',
        verbose_name="Освітня програма",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    form_education = models.CharField(
        verbose_name="Форма навчання",
        max_length=20,
        choices=FormEducationChoice.choices
    )

    update_at = models.DateField(
        verbose_name="Рік коли був відредагований студент",
        default=now,
        null=True
    )

    def __str__(self):
        return f'{self.id} - {self.user.username}'

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"

    @cached_property
    def _year_entry(self):
        entry_date = self.year_entry.strftime("%Y %m %d").split()
        return date(*map(int, entry_date))

    @cached_property
    def group_name(self):
        if hasattr(self.group, 'name'):
            return self.group.name
        return 'ВІДСУТНЯ'

    @hook(BEFORE_CREATE, when='group')
    @hook(BEFORE_UPDATE, when='group')
    def set_educational_program(self):
        self.educational_program = self.group.educational_program
