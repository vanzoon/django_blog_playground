from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

