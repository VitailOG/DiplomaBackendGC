from datetime import date

from methodist.tests.api.schemas.subject import SubjectsSchema
from methodist.tests.api.schemas import BaseSchema, UserSchema
from methodist.models.choices import FormEducationChoice


class StudentGroupSchema(BaseSchema):
    user: UserSchema
    year_entry: date
    group: int
    form_education: FormEducationChoice
    course: int
    educational_program: int


class RatingSchemaMixin(BaseSchema):
    user: int
    subject: int
    date_rating: date
    rating_5: int | None
    rating_12: int | None
    retransmission: bool
    credited: bool
    semester: int
    is_annual_assessment: bool
    teacher: int


class RatingsGroupSchema(RatingSchemaMixin):
    pass


class RatingGroupSchema(SubjectsSchema):
    ratings: list[RatingsGroupSchema] = []
    students: list[StudentGroupSchema] = []
