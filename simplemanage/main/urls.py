from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index', views.index, name='index'),
    path('cliente', views.cliente, name='cliente'),
]
