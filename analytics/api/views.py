from pathlib import Path

from django.http import HttpResponse
from ninja import Router

from analytics.exceptions import DoesNotRegister
from analytics.services import HandlerFactory
from analytics.types import RATING_SYS
from student.security import AuthBearer

from analytics.api.schemas import AnalyticDetailSubjectResponseSchema, GenerateFileRequestSchema
from analytics.repositories.detail_subject import DetailSubjectRepository
from analytics.utils import get_ratings_title

api = Router(
    auth=AuthBearer(), tags=['analytics']
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


@api.post('/analytic-group-by-subject/')
def create_group_by_subject(request, request_data: GenerateFileRequestSchema):
    data = request_data.dict()
    data['user'] = request.auth  # set user in data
    name = data.pop('type_file')  # remove and get type file

    try:
        HandlerFactory.handler(name, **data)()
    except DoesNotRegister:
        return {"Error": True}

    return {"mеssage": "Повідомимо коли файл згенерується, зробити підсвітку чата на фронті"}


@api.post('/download-file/')
def download_file(request, filename: str):
    file = Path(filename)
    if not (file.exists() or file.is_file()):
        return {"message": "file not exist or not file"}

    name = Path(filename).name
    res = Path(filename).open('rb')

    response = HttpResponse(res, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="' + name + '"'
    return response

