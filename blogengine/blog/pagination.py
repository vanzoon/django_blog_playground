from django.core.paginator import Paginator


def pagination(objects: 'QuerySet', requested_page, num_on_page=5) -> dict:
    paginator = Paginator(objects, num_on_page)
    page = paginator.get_page(requested_page)
    next_url = ''
    prev_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'

    return {
        'page_object': page,
        'is_paginated': page.has_other_pages(),
        'next_url': next_url,
        'prev_url': prev_url
    }
