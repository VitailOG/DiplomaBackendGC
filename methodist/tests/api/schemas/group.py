from datetime import date
from decimal import Decimal

from methodist.tests.api.schemas import BaseSchema, UserSchema
from methodist.models.choices import FormEducationChoice


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


class TopStudentSchema(BaseSchema):
    user: UserSchema
    group: int
    form_education: FormEducationChoice
    course: int
    educational_program: int
    total_rating: float
    year_entry: date
    extra_points_students: list[ExtraPointSchema] = []
    student_source: list[StudentSourceSchema] = []
