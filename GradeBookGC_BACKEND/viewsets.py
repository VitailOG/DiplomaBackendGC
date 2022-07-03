from typing import TypeVar, Generic

from rest_framework.serializers import SerializerMetaclass
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .permissions import BasePermission

T = TypeVar('T', bound=BasePermission)


class PermissionView(Generic[T]):
    permission_classes = [T]


class BaseViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
):
    pass


class SerializerClassMixin:
    serializers_map: dict[str, SerializerMetaclass] = None

    def get_serializer_class(self) -> SerializerMetaclass:
        return self.serializers_map.get(getattr(self, 'action'), self.serializers_map['default'])
