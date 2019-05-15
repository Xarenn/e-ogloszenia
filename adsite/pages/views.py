from django.shortcuts import render

def home_view(request, *args, **kwargs):
    return render(request, 'index.html')


def login_view(request, *args, **kwargs):
    return render(request, 'auth/login.html')


def register_view(request, *args, **kwargs):
    return render(request, 'auth/register.html')