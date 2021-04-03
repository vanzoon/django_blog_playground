from django.http import Http404
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrStaffOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            (obj.author == request.user or request.user.is_staff)
        )

class AuthorPermissionMixin:
    def has_permissions(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


