from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class CustomPageNumberPagination(DatatablesPageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 25