from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission as BP
from django.conf import settings

User = get_user_model()


class BasePermission(BP):
    permission_name = None

    def has_permission(self, request, view=None):
        req = getattr(request, 'auth')

        if not isinstance(req, User):
            req = getattr(request, 'user')

        return bool(
            req and req.is_authenticated and req.group.name == self.permission_name
        )


class AllowSwaggerDocsPermissions(BP):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.username == settings.DEVELOPER_USERNAME
        )
