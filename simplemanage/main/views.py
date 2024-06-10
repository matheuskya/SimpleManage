from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from main.forms import LoginForm, ClienteForm, FuncionarioForm, RegistroFinanceiroForm, CardapioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from main.models import Cliente, Funcionario, RegistroFinanceiro, Cardapio
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from heyoo import WhatsApp
import datetime
#Doc pywhatkit: https://github.com/Ankit404butfound/PyWhatKit/wiki/Sending-WhatsApp-Messages
import pywhatkit

# Create your views here.
# sem valores negativos / 0 no campo value do cliente
# criar nomes mais intuitivos para os camps (value!)
#interface (background da table)
#CORES USADAS (FRAPPE):https://github.com/catppuccin/catppuccin

#para realizar as mudancas de tabela (cliente, funcionario, custo) --> teste, ajustar viewList, viewCreate, viewDelete,
#viewUpdate e tables


#comentario para commit de teste
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

# class Login(View):
#     form_class = LoginForm
#     initial = {"key":"value"}
#     template_name = "main/login.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial = self.initial)
#         return render(request, self.template_name, {"login_form":form})
    
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         print(form)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             # if user is not None:
#             #     auth.login(request, user)
#             #     return render(request,'main/index.html')
#             # return render(request, 'main/index.html')
#             return HttpResponse("Funcionou")
#         return HttpResponse("Funcionou")
        
            


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
# @login_required(login_url='login')

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
    model = RegistroFinanceiro

    # def get_clientes(self, request):
    #     model = RegistroFinanceiro.objects.filter(user = request.user)


class ClienteCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "main/cliente/cliente_create.html"
    form_class = RegistroFinanceiroForm
    success_url = "/cliente"

    def form_valid(self, form):
        print('FUNCAO ACESSADA', form.instance.user, self.request.user)
        form.instance.user = self.request.user
        form.instance.category = "cliente"
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    form_class = RegistroFinanceiroForm
    model = RegistroFinanceiro
    template_name = "main/cliente/cliente_update.html"
    success_url = "/cliente"


#hard delete
class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "main/cliente/cliente_delete.html"
    model = RegistroFinanceiro
    success_url = "/cliente"


#soft delete
@login_required(login_url='login')
def cliente_softdelete(request, pk):
    object = RegistroFinanceiro.objects.get(pk = pk)
    context = {
        "object":object
    }
    if (request.method == 'POST'):
        object.state = False
        object.save()
        return redirect('cliente')
    return render(request, 'main/cliente/cliente_delete.html',context)


class FuncionarioListView(LoginRequiredMixin, ListView):
    login_url="login"
    template_name="main/funcionario/funcionario_list.html"
    model = RegistroFinanceiro


class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "main/funcionario/funcionario_create.html"
    form_class = RegistroFinanceiroForm
    success_url = "/funcionario_list"

    def form_valid(self, form):
        print('FUNCAO ACESSADA', form.instance.user, self.request.user)
        form.instance.user = self.request.user
        form.instance.category = "funcionario"
        return super().form_valid(form) 


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    form_class = RegistroFinanceiroForm
    model = RegistroFinanceiro
    template_name = "main/funcionario/funcionario_update.html"
    success_url = "/funcionario_list"


#hard delete
class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "main/funcionario/funcionario_delete.html"
    model = RegistroFinanceiro
    success_url = "/funcionario_list"


#soft delete
@login_required(login_url='login')
def funcionario_softdelete(request, pk):
    object = RegistroFinanceiro.objects.get(pk = pk)
    context = {
        "object":object
    }
    if (request.method == 'POST'):
        object.state = False
        object.save()
        return redirect('funcionario_list')
    return render(request, 'main/funcionario/funcionario_delete.html',context)


class CustoListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "main/custo/custo_list.html"
    model = RegistroFinanceiro


class CustoCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "main/custo/custo_create.html"
    form_class = RegistroFinanceiroForm
    success_url = "/custo_list"

    def form_valid(self, form):
        print('FUNCAO ACESSADA', form.instance.user, self.request.user)
        form.instance.user = self.request.user
        form.instance.category = "custo"
        return super().form_valid(form)


class CustoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    form_class = RegistroFinanceiroForm
    model = RegistroFinanceiro
    template_name = "main/custo/custo_update.html"
    success_url = "/custo_list"


#hard delete
class CustoDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "main/custo/custo_delete.html"
    model = RegistroFinanceiro
    success_url = "/custo_list"


#soft delete
@login_required(login_url='login')
def custo_softdelete(request, pk):
    object = RegistroFinanceiro.objects.get(pk = pk)
    context = {
        "object":object
    }
    if (request.method == 'POST'):
        object.state = False
        object.save()
        return redirect('custo_list')
    return render(request, 'main/custo/custo_delete.html',context)


class CardapioListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "main/cardapio/cardapio_list.html"
    model = Cardapio


class CardapioCreateView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "main/cardapio/cardapio_create.html"
    form_class = CardapioForm
    success_url = "/cardapio_list"
 
    def form_valid(self, form):
        print('FUNCAO ACESSADA', form.instance.user, self.request.user)
        form.instance.user = self.request.user
        form.instance.category = "custo"
        return super().form_valid(form)


class CardapioUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    form_class = CardapioForm
    model = Cardapio
    template_name = "main/cardapio/cardapio_update.html"
    success_url = "/cardapio_list"


class CardapioDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "main/cardapio/cardapio_delete.html"
    model = Cardapio
    success_url = "/cardapio_list"


@login_required(login_url='login')
def adicionar_cardapio(request, pk):
    object = Cardapio.objects.get(pk=pk)
    object.state = not object.state
    object.save()
    print(object)
    context = {
        "object":object,
    }
    return redirect('cardapio_list')


@login_required(login_url='login')
def whats(self, msg_cardapio):
    pywhatkit.sendwhatmsg_instantly("+5543984590897", msg_cardapio, 30, True, 3)
    print(msg_cardapio)
    return redirect("cardapio_list")


@login_required(login_url='login')
def share(request):
    if request.method == "POST":
        context = {}
        msg_cardapio = "Cardapio do dia!: "
        items = request.POST.getlist("obj")
        for item in items:
                msg_cardapio += "\n-" + item
        print(items)
        print(msg_cardapio)
        context = {
            "msg_cardapio":msg_cardapio,
        }
        return render(request, "main/cardapio/cardapio_share.html", context)    
    print("FUNCAO SHARE CHAMADA")
    return render(request, "main/cardapio/cardapio_share.html")    