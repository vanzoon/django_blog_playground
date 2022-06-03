from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from .forms import SignupForm

# TODO: user creation

class SignupView(FormView):
    model = get_user_model()
    form_class = SignupForm
    context_object_name = 'user'
    template_name = 'user_management/signup.html'
    redirect_field_name = 'blog'


class ProfileView(LoginRequiredMixin, TemplateView):
    model = get_user_model()
    context_object_name = 'user'
    template_name = 'user_management/profile.html'

