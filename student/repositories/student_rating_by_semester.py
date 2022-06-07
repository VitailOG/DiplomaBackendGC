from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from methodist.models import Subject, ExtraPoints, Rating


class StudentRatingRepository:

    def __init__(self, semester: int, student_id: int, educational_program_id: int):
        self.semester = semester
        self.student_id = student_id
        self.educational_program_id = educational_program_id

    def _get_ratings(self):
        return Subject.objects.ratings(
            semester=self.semester,
            student_id=self.student_id,
            educational_program_id=self.educational_program_id
        )

    def _get_extra_points(self):
        return ExtraPoints.objects.filter(
            semester=self.semester,
            user_id=self.student_id
        )

    def _calc_sum_extra_points(self):
        extra_point = self._get_extra_points()
        return extra_point.aggregate(point=Coalesce(Sum('point'), 0, output_field=DecimalField()))['point']

    def _calc_sum_ratings(self):
        return Rating.objects.calc_rating_student_by_semester(
            semester=self.semester,
            student_id=self.student_id
        )

    def build_data(self):
        total_rating = self._calc_sum_ratings() + self._calc_sum_extra_points()

        return {
            "ratings": list(self._get_ratings()),
            "extra_points": list(self._get_extra_points()),
            "total_rating": total_rating,
        }
