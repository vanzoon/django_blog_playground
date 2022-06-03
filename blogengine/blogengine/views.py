from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def redirect_to_blog(request):
    return redirect('posts_list_url', permanent=True)

def error_404(request, exception):
    return render(request, '404.html', status=404)


class HomepageView(TemplateView):
    template_name = 'index.html'
    content_type = 'text/html'


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

