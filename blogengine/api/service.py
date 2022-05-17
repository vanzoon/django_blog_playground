from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Paginator(PageNumberPagination):
    max_page_size = 50
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
        {
            'links_to_pages':{
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            },
            'on_page': self.page.paginator.count,
            'results': data
        }
        )
