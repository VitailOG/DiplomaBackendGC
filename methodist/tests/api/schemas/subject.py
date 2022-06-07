from pydantic import HttpUrl

from methodist.tests.api.schemas import (
    BaseSchema,
    EducationalProgramSchema,
    GroupSchema,
    UserSchema
)
from methodist.models.choices import ControlChoice


class SubjectsSchema(BaseSchema):
    group: GroupSchema
    educational_program: EducationalProgramSchema
    teachers: list[UserSchema]
    name_subject: str
    hours: int
    loans: int
    semester: int
    final_semester: int
    form_of_control: ControlChoice
    finally_subject: bool
    url_on_moodle: HttpUrl


class SubjectDetailSchema(BaseSchema):
    name: str
    initial_semester: int
    last_semester: int
    form_of_control: ControlChoice
