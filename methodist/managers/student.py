from typing import Literal

from django.db.models import (
    Manager,
    Q,
    OuterRef,
    Subquery,
    Func,
    Exists,
    When,
    Case,
    Value,
    ExpressionWrapper,
    Prefetch,
    Count,
    Sum,
    DecimalField
)
from django.db.models.functions import Cast, Coalesce, Round
from django.conf import settings

from methodist.constants import CURRENT_YEAR, OTHER_CONTROL

FILTER_BY = Literal[
    'first_name',
    'last_name'
]


class StudentManager(Manager):

    def active_students(self, department):
        """Отримання активних студентів"""
        return self.filter(
            group__isnull=False,
            user__department_id=department.id,
            year_entry__year__range=[CURRENT_YEAR - 4, CURRENT_YEAR]
        )

    def active_students_with_group(self, department):
        return self.active_students(
            department=department
        ).select_related(
            'group'
        )

    def students(self, department):
        """Отримання студентів із детальнию інформацією"""
        return self.active_students_with_group(
            department=department
        ).select_related(
            'educational_program',
            'user'
        )

    def years(self, department):
        """Років вступу"""
        return self.active_students(
            department=department
        ).values(
            'year_entry__year'
        ).distinct()

    def student_info(self, group_id: int):
        return self.select_related(
            'user'
        ).filter(
            group_id=group_id
        )

    def get_values_about_student(self, group_id: int):
        return self.student_info(
            group_id=group_id
        ).values(
            'id',
            'user__username',
            'user__first_name',
            'user__last_name',
        )

    def data_student(self, fio: str, filter_by: FILTER_BY, department):
        """Виведення імя яба прізвища студенів"""

        first_name = Q(user__first_name__icontains=fio)
        last_name = Q(user__last_name__icontains=fio)
        criterion = first_name if filter_by == 'first_name' else last_name

        return self.active_students(
            department=department
        ).filter(
            criterion
        ).values(
            f"user__{filter_by}"
        )

    def rating_list(self, group_id: int, semester: int, is_all_students: bool = False):
        """Рейтинговий список"""
        from methodist.models import Rating, ExtraPoints
        from student.models import StudentSource

        # Отримання додаткових балів
        points = ExtraPoints.objects.filter(
            semester=semester,
            user_id=OuterRef('user_id')
        ).annotate(
            points=Cast(
                Func('point', function='Sum'), output_field=DecimalField()
            )
        ).values(
            'points'
        )

        # Отримання оцінок
        ratings = Rating.objects.filter(
            Q(subject__form_of_control__in=OTHER_CONTROL) | Q(is_annual_assessment=False),
            user_id=OuterRef('pk'),
            semester=semester
        ).annotate(
            rating=Round(
                ExpressionWrapper(
                    # перевірити швидкодію
                    # Cast(Func('rating_5', function='Sum'), output_field=FloatField()) /
                    # Cast(Func('rating_5', function='Count'), output_field=FloatField())
                    Cast(Func('rating_5', function='Avg'), output_field=DecimalField())
                    * settings.COMMON_RATING + Coalesce(Subquery(points), 0),
                    output_field=DecimalField()
                ),
                precision=3
            )
        ).values(
            'rating'
        )

        # Перевірки чи будь-яка форма навчання підходить
        all_students = Q() if is_all_students else Q(form_education="Контрактна")

        # Вивід рейтингового списку
        students = self.student_info(
            group_id=group_id
        ).prefetch_related(
            Prefetch(
                'extra_points_students',
                queryset=ExtraPoints.objects.filter(semester=semester)
            ),
            Prefetch(
                'student_source',
                queryset=StudentSource.objects.filter(semester=semester)
            ),
        ).exclude(
            all_students
        ).alias(
            exists=Exists(ratings),
        ).annotate(
            total_rating=Case(
                When(exists=True, then=Subquery(ratings)),
                When(exists=False, then=Value(0)),
                output_field=DecimalField()
            )
        ).order_by(
            '-total_rating', 'user__last_name', 'user__first_name'
        )

        return students

    def common_rating_for_students(self, group_id: int):
        """Загальний рейтинг для студента по всі річним оцінкам"""
        from methodist.models import Rating

        condition = Q(
            user_rating__is_annual_assessment=True,
            user_rating__subject__finally_subject=True,
            user_rating__rating_12__isnull=True
        )

        return self.student_info(
            group_id=group_id
        ).prefetch_related(
            Prefetch(
                'user_rating',
                queryset=Rating.objects.filter(
                    is_annual_assessment=True, subject__finally_subject=True, rating_12__isnull=True
                ),
            ),
            'user_rating__subject',
            'user_rating__subject__teachers'
        ).annotate(
            total_count=Coalesce(Count('user_rating__rating_5', filter=condition), 0),
            total_sum=Coalesce(Sum('user_rating__rating_5', filter=condition), 0)
        )
