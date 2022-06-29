from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from administration.api.serializers import DepartmentSerializer
from methodist.models import Department


class DepartmentAPI(mixins.ListModelMixin, GenericViewSet):
    my_tags = ["ADMINISTRATION:DEPARTMENT"]
    queryset = Department.objects.prefetch_related('ed_prog_department', 'ed_prog_department__group_ed_prog')
    serializer_class = DepartmentSerializer
