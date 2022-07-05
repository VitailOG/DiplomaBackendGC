from rest_framework.permissions import BasePermission as BP
from django.conf import settings


class BasePermission(BP):
    permission_name = None

    def has_permission(self, request, view=None):
        req = getattr(request, 'auth')

        if not request.path.startswith('/student'):
            req = getattr(request, 'user')

        print(self.permission_name)
        print(req.group.name)

        return bool(
            req and req.is_authenticated and req.group.name == self.permission_name
        )


class AllowSwaggerDocsPermissions(BP):

    def has_permission(self, request, view):
        # return bool(
        #     request.user.is_authenticated and request.user.username == settings.DEVELOPER_USERNAME
        # )
        return True
