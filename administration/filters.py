from django_filters.rest_framework import FilterSet

from methodist.models import CustomUser


class TeacherFilter(FilterSet):

    class Meta:
        model = CustomUser
        fields = ("department",)
