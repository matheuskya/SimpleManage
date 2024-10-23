from django.contrib import admin
from main.models import Cliente, Funcionario, RegistroFinanceiro, Cardapio
# Register your models here.

admin.site.register(RegistroFinanceiro)
# admin.site.register(Cliente)
# admin.site.register(Funcionario)
admin.site.register(Cardapio)
