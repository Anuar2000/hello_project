from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5               # значение по умолчанию
    page_size_query_param = 'page_size'  # позволяет задавать через URL
    max_page_size = 50          # максимум на страницу