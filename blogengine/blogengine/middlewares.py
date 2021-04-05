from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

from blogengine.views import redirect_to_blog


class CheckUserIsBlockedMiddleware(MiddlewareMixin):

    def process_request(self, request, *args, **kwargs):
        if request.user.is_auntificated() and request.user.is_blocked():
            logout(request)
            return redirect(request, redirect_to_blog)