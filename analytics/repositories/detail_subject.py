import operator

from typing import NamedTuple
from django.db import connection


class DetailSubjectRatingCount(NamedTuple):
    cnt: int
    rat: int
    name: str


class DetailSubjectRepository:

    def get_count_rating(
            self, subject_id: int, group_id: int, rating_sys: int = None
    ) -> list[DetailSubjectRatingCount]:

        with connection.cursor() as cursor:
            query = f"""
                select
                    count(r.rating_{rating_sys}) as cnt,
                    r.rating_{rating_sys},
                    s.name_subject
                from methodist_subject as s
                join methodist_rating as r on s.id = r.subject_id
                join methodist_student ms on r.user_id = ms.id
                where s.id={subject_id} and ms.group_id={group_id}
                group by r.rating_{rating_sys}, s.name_subject;
            """
            cursor.execute(query)
            row = cursor.fetchall()

            name_subject = row[0][2]

            data = [DetailSubjectRatingCount(*i) for i in row]

            empty_rating = [
                DetailSubjectRatingCount(
                    name=name_subject, cnt=0, rat=i
                ) for i in range(1, rating_sys + 1) if i not in [i[1] for i in row]
            ]
            data.extend(empty_rating)

            return sorted(data, key=operator.attrgetter('rat'))
