from GradeBookGC_BACKEND.permissions import BasePermission
from GradeBookGC_BACKEND.settings import PermissionGroupChoice


class AdministrationPermission(BasePermission):
    permission_name = PermissionGroupChoice.ADMINISTRATION.value
