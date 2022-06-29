from GradeBookGC_BACKEND.permissions import BasePermission
from GradeBookGC_BACKEND.settings import PermissionGroupChoice


class MethodistPermission(BasePermission):
    permission_name = PermissionGroupChoice.ADMINISTRATION.value
