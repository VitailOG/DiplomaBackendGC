from typing import Literal
from ninja import Router

from analytics.api.schemas import AnalyticDetailSubjectResponseSchema
from analytics.repositories.detail_subject import DetailSubjectRepository
from student.security import AuthBearer


api = Router(
    auth=AuthBearer(),
    tags=['analytics']
)


@api.get('/')
def semesters_for_student(request):
    return {}


RATING_SYS = Literal[
    5,
    12
]


@api.get('/{group_id}/{subject_id}/', response=AnalyticDetailSubjectResponseSchema)
def group_detail(request, group_id: int, subject_id: int, rating_sys: int = 5):
    r = DetailSubjectRepository()
    s = r.get_count_rating(subject_id, group_id, rating_sys)
    return {
        "cnt_rating": s
    }
