from rest_framework.pagination import LimitOffsetPagination


class BasePagination(LimitOffsetPagination):
    default_limit = 5
