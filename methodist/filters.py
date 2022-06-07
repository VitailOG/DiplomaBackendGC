from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    NumberFilter
)

from methodist.models.users import Student
from methodist.models.subject import Subject


class StudentFilter(FilterSet):

    first_name = CharFilter(field_name="user__first_name", lookup_expr="icontains")
    last_name = CharFilter(field_name="user__last_name", lookup_expr="icontains")

    min_year = NumberFilter(
        field_name="year_entry__year",
        lookup_expr="gte",
        label="Початковий"
    )
    max_year = NumberFilter(
        field_name="year_entry__year",
        lookup_expr="lte",
        label="Кінцевий"
    )

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'group',
            'educational_program',
            'form_education',
            'min_year',
            'max_year',
        )


class SubjectFilter(FilterSet):
    subject = CharFilter(field_name="name_subject", lookup_expr="icontains")

    class Meta:
        model = Subject
        fields = (
            "subject",
            "group",
            "semester",
            'educational_program',
            "final_semester",
            "teachers"
        )
