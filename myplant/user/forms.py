from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'nickname', 'location', 'email']

class CustomUserChangeForm(UserChangeForm):
    password = None        
    username = forms.CharField(label='아이디', widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField(label='이메일', required=False)
    nickname = forms.CharField(label='닉네임')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nickname']