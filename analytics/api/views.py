from typing import Literal

from ninja import Router

from analytics.types import RATING_SYS
from student.security import AuthBearer

from analytics.api.schemas import AnalyticDetailSubjectResponseSchema
from analytics.repositories.detail_subject import DetailSubjectRepository
from analytics.utils import get_ratings_title

api = Router(
    # auth=AuthBearer(),
    tags=['analytics']
)


@api.get(
    '/{group_id}/{subject_id}/',
    response=AnalyticDetailSubjectResponseSchema
)
def group_detail(request, group_id: int, subject_id: int, rating_sys: RATING_SYS):
    rating_sys = int(rating_sys)

    repository = DetailSubjectRepository(subject_id=subject_id, group_id=group_id)
    s = repository.get_count_rating(rating_sys=rating_sys)
    return {
        "cnt_rating": s,
        "rating_title": get_ratings_title(rating_sys)
    }
