from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from methodist.models import Department
from methodist.api.serializers import CustomUserSerializer
from administration.api.permisions import AdministrationPermission
from administration.api.serializers import (
    DepartmentWithEducationProgramSerializer,
    DepartmentSerializer,
    TeacherDetailSerializer
)
from administration.filters import TeacherFilter


User = get_user_model()


class DepartmentAPI(mixins.ListModelMixin, GenericViewSet):
    my_tags = ["ADMINISTRATION:DEPARTMENT"]
    permission_classes = [AdministrationPermission]
    queryset = Department.objects.all()

    @action(methods=['get'], detail=False, url_path="with-education-and-group")
    def get_department(self, *args, **kwargs):
        departments = Department.objects.prefetch_related('ed_prog_department', 'ed_prog_department__group_ed_prog')
        data = self.get_serializer(departments, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        serializers = {
            "get_department": DepartmentWithEducationProgramSerializer,
            "list": DepartmentSerializer,
        }
        return serializers.get(self.action, serializers['list'])


class TeacherAPI(ReadOnlyModelViewSet):
    my_tags = ["ADMINISTRATION:TEACHER"]
    queryset = User.objects.teachers()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
    permission_classes = [AdministrationPermission]

    def get_serializer_class(self):
        serializers = {
            "retrieve": TeacherDetailSerializer,
            "list": CustomUserSerializer,
        }
        return serializers.get(self.action, serializers['list'])

