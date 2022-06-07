from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, F, Sum
from django_lifecycle import LifecycleModel, hook, BEFORE_CREATE, BEFORE_UPDATE
from django_lifecycle.decorators import DjangoLifeCycleException

from . import Group
from .choices import SemesterChoice, ControlChoice
from methodist.managers import subject, rating


class Subject(LifecycleModel):

    objects = subject.SubjectManager()

    name_subject = models.CharField(verbose_name="Назва предмета", max_length=60)

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Група"
    )

    teachers = models.ManyToManyField('CustomUser', verbose_name="Викладачі", related_name='user_teacher')

    hours = models.PositiveIntegerField(verbose_name="Кількість годин")

    loans = models.PositiveIntegerField(verbose_name="Кількість кредитів", blank=True)

    semester = models.IntegerField(
        verbose_name="Семестр",
        choices=SemesterChoice.choices
    )

    educational_program = models.ForeignKey(
        'EducationalProgram',
        verbose_name="Освітня програма",
        on_delete=models.CASCADE,
        null=True
    )

    final_semester = models.IntegerField(
        verbose_name="Кінцевий семестр",
        null=True,
        blank=True,
        choices=SemesterChoice.choices
    )

    form_of_control = models.CharField(
        verbose_name="Форма конролю",
        max_length=20,
        choices=ControlChoice.choices
    )

    url_on_moodle = models.URLField()

    finally_subject = models.BooleanField(default=False, verbose_name="Фінальний предмет")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(final_semester__gte=F('semester'))
                ),
                name='semester'
            ),
            models.UniqueConstraint(
                fields=['name_subject', 'group'],
                name='name_subject_unique'
            )
        ]
        ordering = ['-id']

    def clean(self):
        if self.final_semester < self.semester:
            raise ValidationError({"final_semester": "error"})

    def __str__(self):
        return self.name_subject

    def save(self, *args, **kwargs):
        self.loans = self.hours // 2
        if self.final_semester is None:
            self.final_semester = self.semester

        super().save(*args, **kwargs)

    @hook(BEFORE_CREATE, when='group')
    @hook(BEFORE_UPDATE, when='group')
    def set_educational_program(self):
        name = self.name_subject.split(' (')
        self.educational_program = self.group.educational_program
        self.name_subject = f'{name[0]} ({self.group.name})'


class Rating(models.Model):
    """ Оцінки студентів
    """

    objects = rating.RatingManager()

    user = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        verbose_name="Студент",
        related_name='user_rating'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет"
    )

    date_rating = models.DateField(verbose_name="Дата оцінки")

    rating_5 = models.PositiveIntegerField(
        verbose_name="Оцінка 5",
        null=True,
        blank=True
    )
    rating_12 = models.PositiveIntegerField(
        verbose_name="Оцінка 12",
        null=True,
        blank=True
    )

    retransmission = models.BooleanField(verbose_name="Перездача", default=False)

    credited = models.BooleanField(verbose_name="Зараховано", default=False)

    semester = models.PositiveIntegerField(
        verbose_name="Семестер",
        null=True,
        blank=True
    )

    is_annual_assessment = models.BooleanField(verbose_name="Річна оцінка", default=False)

    teacher = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name="teacher"
    )

    def __str__(self):
        return f"{self.user} оцінка {self.rating_5} з {self.subject.name_subject} в {self.semester}"

    def save(self, *args, **kwargs):
        dict_rating = {
            (1, 2, 3): 2,
            (4, 5, 6): 3,
            (7, 8, 9): 4,
            (10, 11, 12): 5
        }

        if self.rating_12 is not None:
            for i in dict_rating.keys():
                if self.rating_12 in i:
                    self.rating_5 = dict_rating.get(i)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        constraints = [
            models.CheckConstraint(
                check=(
                    ~Q(rating_5__isnull=True, rating_12__isnull=True)
                ),
                name='rating'
            ),
            models.CheckConstraint(
                check=(
                    Q(semester__gte=1, semester__lte=8)
                ),
                name='semester_check'
            ),
            models.UniqueConstraint(
                fields=['user', 'subject', 'semester', 'is_annual_assessment'],
                name='rating_unique'
            )
        ]


class ExtraPoints(LifecycleModel):
    """ Extra points by semester
    """

    user = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
        verbose_name="Студент",
        related_name='extra_points_students'
    )

    semester = models.PositiveIntegerField(verbose_name="Семестер")

    point = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Додаткові бали')

    text = models.TextField(verbose_name='Коротка рецензія')

    class Meta:
        verbose_name = "Додатковий бал"
        verbose_name_plural = "Додаткові бали"
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(point__gt=0.0, point__lte=0.5)
                ),
                name='point_check'
            )
        ]

    def __str__(self):
        return f"{self.user} in {self.semester} - {self.point}"

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def check_amount_extra_points(self):

        extra_point = ExtraPoints.objects.filter(
            semester=self.semester, user=self.user
        ).aggregate(
            point=Sum('point')
        )['point'] or 0

        if self.pk:
            extra_point -= self.initial_value('point')

        if Decimal(str(extra_point)) + self.point > 0.5:
            raise DjangoLifeCycleException({"error": 'Додатковий бал не повинен перевищувати - 0.5', "status": 500})
