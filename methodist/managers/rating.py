from decimal import Decimal

from django.db.models import Manager, Avg, Q, DecimalField
from django.db.models.functions import Cast, Coalesce
from django.conf import settings

from methodist.constants import OTHER_CONTROL


class RatingManager(Manager):

    def get_semesters_student(self, student_id: int):
        """Отримання всі семестрів окремого студента"""
        return self.filter(
                user_id=student_id
            ).values_list(
                'semester', flat=True
            ).order_by(
                '-semester'
            ).distinct()

    def get_ratings_by_subject(self, subject_id: int, group_id: int, semester: int = None):
        """Отримання всіх оцінок придмету"""
        query = self.filter(
            user__group_id=group_id,
            subject_id=subject_id,
        ).order_by(
            'semester'
        )

        if semester is not None:
            query = query.filter(semester=semester)
        return query

    def calc_rating_student_by_semester(self, student_id: int, semester: int):
        """Рахування семестрового балу для студента"""
        return self.filter(
                Q(subject__form_of_control__in=OTHER_CONTROL) | Q(is_annual_assessment=False),
                user_id=student_id,
                semester=semester,
            ).aggregate(
                rating=Cast(
                    Coalesce(Avg('rating_5'), 0), output_field=DecimalField()
                )
            )['rating'] * Decimal(f'{settings.COMMON_RATING}')

    def get_rating_info(self, subject_id: int, group_id: int, semester: int, rating: int):
        return self.filter(
            subject_id=subject_id,
            user__group_id=group_id,
            semester=semester
        ).values(
            'user_id',
            f'rating_{rating}',
            'credited',
            'retransmission'
        )
