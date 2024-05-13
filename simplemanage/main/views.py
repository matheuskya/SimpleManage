from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from main.forms import LoginForm, ClienteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from main.models import Cliente, Funcionario
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

# Create your views here.
# sem valores negativos / 0 no campo value do cliente
# criar nomes mais intuitivos para os camps (value!)
#interface (background da table)
#CORES USADAS (FRAPPE):https://github.com/catppuccin/catppuccin



def teste(request):

    return HttpResponse('pagina teste')


def login(request):
    login_form = LoginForm()
    if (request.method == "POST"):
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')

    context = {
        "login_form": login_form,
    }
    return render(request, 'main/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    date = datetime.datetime.now()
    datestr = date.strftime("%c")
    print(datestr)
    context = {
        "datestr":datestr
    }
    return render(request, 'main/index.html', context)


# @login_required(login_url='login')
# def cliente(request):
#     cliente_form = ClienteForm()
#     cliente_list = Cliente.objects.all()

#     if (request.method == 'POST'):
#         cliente_form = ClienteForm(request.POST)
#         if cliente_form.is_valid():
#             cliente = cliente_form.save(commit=False)
#             cliente.user = request.user
#             cliente.save()
#             return redirect('index')
#     else:
#         context = {
#             "cliente_list":cliente_list,
#         }
#         return render(request, 'main/cliente.html', context)


# @login_required(login_url='login')
# def cliente_post(request):
#     cliente_form = ClienteForm()
#     context={
#         "cliente_form":cliente_form
#     }
#     if (request.method == 'POST'):
#         cliente_form = ClienteForm(request.POST)
#         if cliente_form.is_valid():
#             cliente = cliente_form.save(commit=False)
#             cliente.user = request.user
#             cliente.save()
#             return redirect('index')
#     return render(request, 'main/cliente_create.html', context)


class ClienteListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "main/cliente/cliente_list.html"
    model = Cliente


class ClienteCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "main/cliente/cliente_create.html"
    form_class = ClienteForm
    success_url = "/cliente"

    def form_valid(self, form):
        print('FUNCAO ACESSADA', form.instance.user, self.request.user)
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    fields = ["name", "description", "value"]
    model = Cliente
    template_name = "main/cliente/cliente_update.html"
    success_url = "/cliente"


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "main/cliente/cliente_delete.html"
    model = Cliente
    success_url = "/cliente"


class FuncionarioListView(LoginRequiredMixin, ListView):
    login_url="login"
    template_name="main/funcionario/funcionario_list.html"
    model = Funcionario