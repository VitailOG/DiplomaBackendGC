from datetime import date

from methodist.tests.api.schemas import (
    BaseSchema,
    GroupSchema,
    EducationalProgramSchema,
    UserSchema
)


class StudentListSchema(BaseSchema):
    group: GroupSchema
    educational_program: EducationalProgramSchema
    user: UserSchema
    form_education: str
    course: int
    year_entry: date
