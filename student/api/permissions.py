from GradeBookGC_BACKEND.permissions import BasePermission
from GradeBookGC_BACKEND.settings import PermissionGroupChoice


class StudentPermission(BasePermission):
    permission_name = PermissionGroupChoice.STUDENT.value
