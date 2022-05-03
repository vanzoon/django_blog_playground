from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

# Create your views here.
class UserCreationForm(UserCreationForm):
    model = User
    fields = ['email', 'username']


class UserChangeForm(UserChangeForm):
    model = User
    fields = ['email', 'username']

