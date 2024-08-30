from django.contrib import admin
from django.urls import path
from main import views
# from main.views import ClienteListView

urlpatterns = [
    path('', views.login, name='login'),
    # path('', views.Login.as_view(), name='login'),
    path('logout',views.logout_view, name="logout"),
    path('index', views.index, name='index'),

    path('cliente', views.ClienteListView.as_view(), name='cliente'),
    path('cliente/create',views.ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/<int:pk>/update', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/<int:pk>/delete', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    path('cliente/<int:pk>/softdelete', views.cliente_softdelete, name='cliente_softdelete'),
    path('cliente/<int:pk>/value_update', views.ClienteValueUpdateView.as_view(), name='cliente_value_update'),


    path('funcionario_list', views.FuncionarioListView.as_view(), name='funcionario_list'),
    path('funcionario/create', views.FuncionarioCreateView.as_view(), name='funcionario_create'),
    path('funcionario/<int:pk>/update', views.FuncionarioUpdateView.as_view(), name='funcionario_update'),
    path('funcionario/<int:pk>/delete', views.FuncionarioDeleteView.as_view(), name='funcionario_delete'),
    path('funcionario/<int:pk>/softdelete', views.funcionario_softdelete, name='funcionario_softdelete'),


    path('cardapio_list', views.CardapioListView.as_view(), name='cardapio_list'),
    path('cardapio/create', views.CardapioCreateView.as_view(), name='cardapio_create'),
    path('cardapio/<int:pk>/update', views.CardapioUpdateView.as_view(), name='cardapio_update'),
    path('cardapio/<int:pk>/delete', views.CardapioDeleteView.as_view(), name='cardapio_delete'),
    path('cardapio/adicionar_cardapio/<int:pk>', views.adicionar_cardapio, name='adicionar_cardapio'),
    path("whats/<str:msg_cardapio>", views.whats, name="whats"),
    path("share", views.share, name="share"),
    path("menu_download", views.menu_download, name="menu_download"),
    path("menu_clear", views.menu_clear, name="menu_clear"),


    path('custo_list', views.CustoListView.as_view(), name='custo_list'),
    path('custo/create', views.CustoCreateView.as_view(), name='custo_create'),
    path('custo/<int:pk>/update', views.CustoUpdateView.as_view(), name='custo_update'),
    path('custo/<int:pk>/delete', views.CustoDeleteView.as_view(), name='custo_delete'),
    path('custo/<int:pk>/softdelete', views.custo_softdelete, name='custo_softdelete'),
]
