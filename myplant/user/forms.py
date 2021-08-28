from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'nickname', 'location', 'email']