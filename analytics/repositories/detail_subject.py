import operator

from django.db import connection
from django.db.models import Avg

from analytics.types import DetailSubjectRatingCount
from analytics.utils import Percentile
from methodist.models import Subject


class DetailSubjectRepository:

    def __init__(self, subject_id: int, group_id: int):
        self.subject_id = subject_id
        self.group_id = group_id

    def get_count_rating(self, rating_sys: int = None) -> list[DetailSubjectRatingCount]:

        with connection.cursor() as cursor:
            query = f"""
                select
                    count(r.rating_{rating_sys}) as cnt,
                    r.rating_{rating_sys}
                from methodist_subject as s
                join methodist_rating as r on s.id = r.subject_id
                join methodist_student ms on r.user_id = ms.id
                where s.id={self.subject_id} and ms.group_id={self.group_id}
                group by r.rating_{rating_sys}, s.name_subject;
            """
            cursor.execute(query)
            row = cursor.fetchall()

            def present_data(info: list[DetailSubjectRatingCount]) -> list[DetailSubjectRatingCount]:
                data = [DetailSubjectRatingCount(*i) for i in info]

                empty_rating = [
                    DetailSubjectRatingCount(
                       cnt=0, rat=i
                    ) for i in range(1, rating_sys + 1) if i not in [i[1] for i in info]
                ]

                data.extend(empty_rating)

                return sorted(data, key=operator.attrgetter('rat'))

            return present_data(row)

    def get_avg_and_median_rating_by_subject(self):
        return Subject.objects.filter(
            id=self.subject_id, group_id=self.group_id
        ).aggregate(
            avg_rating=Avg('rating__rating_5'),
            median_rating_50=Percentile('rating__rating_5', percentile=0.5),
            median_rating_25=Percentile('rating__rating_5', percentile=0.2),
            median_rating_75=Percentile('rating__rating_5', percentile=0.75)
        )
