from decimal import Decimal
from datetime import date

from ninja import Schema


class BaseSchema(Schema):
    id: int


class UserSchema(BaseSchema):
    fio: str

    def resolve_fio(self, obj):
        return f'{obj.last_name} {obj.first_name[0].title()}.{obj.surname[0].title()}.'


class StudentSchema(BaseSchema):
    user: UserSchema


class RatingSchema(BaseSchema):
    rating_5: int
    rating_12: int | None
    retransmission: bool
    credited: bool
    teacher: UserSchema
    user: StudentSchema
    date_rating: date
    is_annual_assessment: bool
    is_annual: bool


class ExtraPointsSchema(BaseSchema):
    id: int
    point: Decimal
    text: str


class SubjectSchema(BaseSchema):
    name_subject: str
    form_of_control: str
    rating_set: list[RatingSchema] = []


class StudentRatingsResponseSchema(Schema):
    ratings: list[SubjectSchema] = []
    extra_points: list[ExtraPointsSchema] = []
    total_rating: float | None


class SemestersResponseSchema(Schema):
    semesters: list = []


class ConvertTextToAudioRequestSchema(Schema):
    text: str
    lang: str = 'uk'
    slow: bool = False
