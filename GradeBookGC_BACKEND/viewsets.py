from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class BaseViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
):
    pass
