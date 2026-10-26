from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class ReviewListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3


class CustomCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-created'
