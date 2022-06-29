from rest_framework.serializers import ModelSerializer

from methodist.models import Department, EducationalProgram
from methodist.api.serializers import GroupSerializer


class EducationProgramSerializer(ModelSerializer):
    group_ed_prog = GroupSerializer(many=True)

    class Meta:
        model = EducationalProgram
        fields = "__all__"


class DepartmentSerializer(ModelSerializer):
    """ Department serializer with education programs and groups """
    ed_prog_department = EducationProgramSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"
