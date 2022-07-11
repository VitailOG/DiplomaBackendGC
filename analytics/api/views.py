from ninja import Router

from analytics.services import HandlerFactory
from analytics.services.excel import ExcelService
from student.security import AuthBearer


api = Router(
    # auth=AuthBearer(),
    tags=['analytics']
)


@api.get('/')
def semesters_for_student(request):
    print(HandlerFactory.handlers)
    return {}
