from ninja import Router

from student.security import AuthBearer


api = Router(
    auth=AuthBearer(), tags=['analytics']
)

