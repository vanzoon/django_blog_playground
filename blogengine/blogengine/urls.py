from django.contrib import admin
from django.urls import path, include, re_path

from blog.views import ProfileView
from . import settings
from .views import redirect_to_blog, RobotsTxtView
from send_email.views import ContactView

# TODO: profile template needed


urlpatterns = [
    path('', redirect_to_blog),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('blog/', include('blog.urls')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('robots.txt', RobotsTxtView.as_view()),
    re_path('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
