from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput
from main.models import Cliente, Funcionario, RegistroFinanceiro


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), label='Usuario')
    password = forms.CharField(widget=PasswordInput(), label='Senha')


class RegistroFinanceiroForm(ModelForm):

    class Meta:
        model = RegistroFinanceiro
        fields = ['name', 'value', 'description']
        labels = {
            "name": "Nome",
            "description": "Detalhes",
            "value": "Conta"
        }



class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = ['name', 'value', 'description']
        labels = {
            "name": "Nome",
            "description": "Detalhes",
            "value": "Conta"
        }


class FuncionarioForm(ModelForm):

    class Meta:
        model = Funcionario
        fields = ['name', 'value', 'description']
        labels = {
            "name": "Nome do funcionario",
            "description": "Detalhes",
            "value": "Conta",
        }
