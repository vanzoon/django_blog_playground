from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from send_email.views import ContactView
from .settings import DEBUG
from .views import redirect_to_blog, RobotsTxtView

# TODO: profile template needed


urlpatterns = [
    path('', redirect_to_blog),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('robots.txt', RobotsTxtView.as_view()),
    url('', include('social_django.urls', namespace='social'))
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
