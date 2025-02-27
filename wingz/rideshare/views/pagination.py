"""For paginators"""

from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    """Custom pagination class."""

    page_size = 10
    page_size_query_param = "page_size"  # Allow client to override
    max_page_size = 50
