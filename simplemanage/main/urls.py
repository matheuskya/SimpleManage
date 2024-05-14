from django.contrib import admin
from django.urls import path
from main import views
# from main.views import ClienteListView

urlpatterns = [
    path('', views.login, name='login'),
    path('teste', views.teste, name='teste'),
    path('logout',views.logout_view, name="logout"),
    path('index', views.index, name='index'),

    path('cliente', views.ClienteListView.as_view(), name='cliente'),
    path('cliente/create',views.ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/<int:pk>/update', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/<int:pk>/delete', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    path('funcionario_list', views.FuncionarioListView.as_view(), name='funcionario_list'),
    path('funcionario/create', views.FuncionarioCreateView.as_view(), name='funcionario_create'),
    path('funcionario/<int:pk>/update', views.FuncionarioUpdateView.as_view(), name='funcionario_update'),
    path('funcionario/<int:pk>/delete', views.FuncionarioDeleteView.as_view(), name='funcionario_delete')
]
