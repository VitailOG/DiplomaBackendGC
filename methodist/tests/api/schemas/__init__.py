from pydantic import Extra
from ninja import Schema


class BaseSchema(Schema):
    id: int

    class Config:
        extra = Extra.forbid


class GroupSchema(BaseSchema):
    name: str
    semesters: list[int] | None


class EducationalProgramSchema(BaseSchema):
    name: str


class UserSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    surname: str
    department: int
