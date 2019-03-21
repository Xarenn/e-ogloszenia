from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .models import Ad
from .forms import SignUpForm, AddAdForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def add_ad(request):
    if request.method == 'POST':
        form = AddAdForm(request.POST)
        if form.is_valid():
            ad = Ad(title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            ad.user = request.user
            ad.save()
            return redirect('home')
    else:
        form = AddAdForm()
    return render(request, 'ads/add_ad.html', {'form': form})


def ads_view(request):
    ads = Ad.objects.all()
    template = loader.get_template('home.html')
    paginator = Paginator(ads, 6)
    page = request.GET.get('page')
    ads_list = paginator.get_page(page)
    context = {
        'ads_list': ads_list,
    }
    return HttpResponse(template.render(context, request))