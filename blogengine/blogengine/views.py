from django.shortcuts import redirect
from django.views.generic import TemplateView

from blog.models import Post, Tag

# TODO: finish to implement sitemap and robots views


def redirect_to_blog():
    return redirect('posts_list_url', permanent=True)


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
# or even
# path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),


class SitemapXmlView(TemplateView):
    template_name = 'sitemap_xml.html'
    content_type = 'application/xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['tags'] = Tag.objects.all()
        return context
