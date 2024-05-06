from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from main.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login(request):
    login_form = LoginForm()
    if (request.method == "POST"):
        login_form = LoginForm(request, data=request.POST)
        print("PRINTTTTTTTT")
        print(login_form)

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


def index(request):
    context = {

    }
    return render(request, 'main/index.html', context)
