from datetime import date
from decimal import Decimal

from methodist.tests.api.schemas import BaseSchema, UserSchema
from methodist.models.choices import FormEducationChoice
from methodist.tests.api.schemas.rating import RatingSchemaMixin
from methodist.tests.api.schemas.subject import SubjectSchemaMixin


class ExtraPointSchema(BaseSchema):
    semester: int
    point: Decimal
    text: str
    user: int


class UserWithYearEntrySchema(UserSchema):
    year_entry: date


class StudentSourceSchema(BaseSchema):
    student: int
    file: str


class GroupSchemaMixin(BaseSchema):
    user: UserSchema
    group: int
    educational_program: int
    year_entry: date
    form_education: FormEducationChoice


class TopStudentSchema(GroupSchemaMixin):
    course: int
    total_rating: float
    extra_points_students: list[ExtraPointSchema] = []
    student_source: list[StudentSourceSchema] = []


class SubjectSchema(SubjectSchemaMixin):
    group: int
    educational_program: int


class UserRatingSchema(RatingSchemaMixin):
    name_subject: str
    subject: SubjectSchema


class CommonRatingSchema(GroupSchemaMixin):
    total_sum: int = 0
    total_count: int = 0
    user_rating: list[UserRatingSchema] = []
