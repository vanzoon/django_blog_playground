from django.shortcuts import redirect
from django.views.generic import TemplateView

from blog.models import Post, Tag


def redirect_to_blog(request):
    return redirect('posts_list_url', permanent=True)


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
