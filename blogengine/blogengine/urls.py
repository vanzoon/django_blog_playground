from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import settings
from .views import redirect_to_blog, RobotsTxtView
from send_email.views import ContactView

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

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
