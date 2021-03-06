from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import AppUser


class RegisterForm(UserCreationForm):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль...'})
    )
    password2 = forms.CharField(
        label='Пароль еще раз',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль еще раз...'})
    )

    class Meta:
        model = AppUser
        fields = ['email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль...'})
    )
