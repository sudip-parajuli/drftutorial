from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

# class ReviewListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'  # Allow clients to set page size via query param


# class CustomLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 2  # Default number of items
#     max_limit = 3     # Maximum limit user can set


class CustomCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-created'