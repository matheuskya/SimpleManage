from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), label='Usuario')
    password = forms.CharField(widget=PasswordInput(), label='Senha')
