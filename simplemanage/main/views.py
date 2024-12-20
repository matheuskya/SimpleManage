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
# from heyoo import WhatsApp
import datetime
#Doc pywhatkit: https://github.com/Ankit404butfound/PyWhatKit/wiki/Sending-WhatsApp-Messages
# import pywhatkit
#doc pillow: https://pillow.readthedocs.io/en/stable/
from main.utils import *
from django.db.models import Q


# Create your views here.
# sem valores negativos / 0 no campo value do cliente
# criar nomes mais intuitivos para os camps (value!)
#interface (background da table)
#CORES USADAS (FRAPPE):https://github.com/catppuccin/catppuccin

#para realizar as mudancas de tabela (cliente, funcionario, custo) --> teste, ajustar viewList, viewCreate, viewDelete,
#viewUpdate e tables


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
# @login_required(login_url='login')

@login_required(login_url='login')
def index(request):
    date = datetime.now()
    datestr = date.strftime("%d/%m/%y %H:%M:%S")
    context = {
        "datestr":datestr
    }

    #instanciando graficos e cards eenviando pro contexto
    #cards de valor
    registrofinanceiro_value = create_value_card("", request)
    context["registrofinanceiro_value"] = registrofinanceiro_value
    cliente_value = create_value_card("cliente", request)
    context["cliente_value"] = cliente_value
    funcionario_value = create_value_card("funcionario", request)
    context["funcionario_value"] = funcionario_value
    custo_value = create_value_card("custo", request)
    context["custo_value"] = custo_value

    #cards de entrada
    total_clientes_card = create_active_card("cliente", request)
    context["total_clientes_card"] = total_clientes_card

    total_funcionarios_card = create_active_card("funcionario", request)
    context["total_funcionarios_card"] = total_funcionarios_card
    total_custos_card = create_active_card("custo", request)
    context["total_custos_card"] = total_custos_card

    #charts
    chart_registrofinanceiro = create_registrofinanceiro_chart("Custos totais", request)
    context["chart_registrofinanceiro"] = chart_registrofinanceiro
    bar_chart = create_monthly_expense_chart(request)
    context["bar_chart"] = bar_chart



    return render(request, 'main/index.html', context)


class ClienteListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "main/cliente/cliente_list.html"
    model = RegistroFinanceiro

    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(category='cliente').filter(user=self.request.user)

    #     order = self.request.GET.get('order', 'asc')
    #     sort_by = self.request.GET.get('sort', 'name')

    #     if order == "desc":
    #         sort_by = f'-{sort_by}'

    #     queryset= queryset.order_by(sort_by)
    #     return queryset
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='cliente').filter(user=self.request.user)

        # Get search query from URL parameters
        search_query = self.request.GET.get('search', '')

        # Apply search filter if there's a query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            # Existing sorting logic
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'name')

        if order == "desc":
            sort_by = f'-{sort_by}'

        queryset = queryset.order_by(sort_by)
        return queryset
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search_query'] = self.request.GET.get('search', '')
            return context


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

class ClienteValueUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    form_class = RegistroFinanceiroForm
    model = RegistroFinanceiro
    template_name = "main/cliente/cliente_update.html"
    success_url = "/cliente"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only display the 'value' field, or whichever field you want
        form.fields = {'value': form.fields['value']}
        return form




class FuncionarioListView(LoginRequiredMixin, ListView):
    login_url="login"
    template_name="main/funcionario/funcionario_list.html"
    model = RegistroFinanceiro
    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(category='funcionario').filter(user=self.request.user)

    #     order = self.request.GET.get('order', 'asc')
    #     sort_by = self.request.GET.get('sort', 'name')

    #     if order == "desc":
    #         sort_by = f'-{sort_by}'

    #     queryset= queryset.order_by(sort_by)
    #     return queryset
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='funcionario').filter(user=self.request.user)

        # Get search query from URL parameters
        search_query = self.request.GET.get('search', '')

        # Apply search filter if there's a query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            # Existing sorting logic
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'name')

        if order == "desc":
            sort_by = f'-{sort_by}'

        queryset = queryset.order_by(sort_by)
        return queryset
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search_query'] = self.request.GET.get('search', '')
            return context

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
    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(category='custo').filter(user=self.request.user)

    #     order = self.request.GET.get('order', 'asc')
    #     sort_by = self.request.GET.get('sort', 'name')

    #     if order == "desc":
    #         sort_by = f'-{sort_by}'

    #     queryset= queryset.order_by(sort_by)
    #     return queryset
    def get_queryset(self):
        queryset = super().get_queryset().filter(category='custo').filter(user=self.request.user)

        # Get search query from URL parameters
        search_query = self.request.GET.get('search', '')

        # Apply search filter if there's a query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            # Existing sorting logic
        order = self.request.GET.get('order', 'asc')
        sort_by = self.request.GET.get('sort', 'name')

        if order == "desc":
            sort_by = f'-{sort_by}'

        queryset = queryset.order_by(sort_by)
        return queryset
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search_query'] = self.request.GET.get('search', '')
            return context

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
    extra_context = {"second_div" : True}
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


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
def menu_clear(request):
    object = Cardapio.objects.filter(state=1)
    for i in object:
        i.state = not i.state
        i.save()
    return redirect('cardapio_list')


#enviar o cardapio em texto via whatsapp
# @login_required(login_url='login')
# def whats(self, msg_cardapio):
#     pywhatkit.sendwhatmsg_instantly("+5543984590897", msg_cardapio, 30, True, 3)
#     print(msg_cardapio)
#     return redirect("cardapio_list")


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


@login_required(login_url="login")
def menu_download(request):
    if request.method == "POST":
        menu_date = request.POST.get("menu_date")
        img = generate_menu_image(menu_date)
        print(menu_date)
        #prepara a imagem para download
        response = HttpResponse(content_type = "image/png")
        response["Content-Disposition"]="attachment; filename='cardapio.png'"
        img.save(response, "PNG")
        return response
