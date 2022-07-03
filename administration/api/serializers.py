from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from methodist.models import Department, EducationalProgram, Subject
from methodist.api.serializers import GroupSerializer

User = get_user_model()


class EducationProgramSerializer(ModelSerializer):
    group_ed_prog = GroupSerializer(many=True)

    class Meta:
        model = EducationalProgram
        fields = "__all__"


class DepartmentWithEducationProgramSerializer(ModelSerializer):
    """ Department serializer with education programs and groups """
    ed_prog_department = EducationProgramSerializer(many=True)

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentSerializer(ModelSerializer):
    """ Department serializer """

    class Meta:
        model = Department
        fields = "__all__"


class SubjectForTeacherSerializer(ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            "id", "name_subject"
        )


class TeacherDetailSerializer(ModelSerializer):
    department = DepartmentSerializer()
    user_teacher = SubjectForTeacherSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "surname", "last_name", "department", "user_teacher"
        )
