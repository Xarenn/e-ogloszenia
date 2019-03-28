from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from accounts.account_service import get_ads_by_username
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
            return redirect('success_register')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def success_signup(request):
    return render(request, 'registration/register_success.html')


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
    ads_list_promoted = ads[:3]
    template = loader.get_template('home.html')
    paginator = Paginator(ads, 9)
    page = request.GET.get('page')
    ads_list = paginator.get_page(page)
    context = {
        'ads_list': ads_list,
        'ads_list_promoted': ads_list_promoted
    }
    return HttpResponse(template.render(context, request))


def ad_view(request, ad_id):
    ad = Ad.objects.filter(pk=ad_id)
    template = loader.get_template('ads/ad_view.html')
    context = {
        'ad': ad[0]
    }
    return HttpResponse(template.render(context, request))


def search(request):
    ads = Ad.objects.all()
    query = request.GET.get('q')
    ads_filtered = Ad.objects.filter(Q(title__icontains=query))
    ads_list_promoted = ads[:3]
    paginator = Paginator(ads_filtered, 9)
    page = request.GET.get('page')
    ads_list_filtered = paginator.get_page(page)
    return render(request, 'home.html', {'ads_list': ads_list_filtered, 'ads_list_promoted': ads_list_promoted})


def your_ads(request):
    username = request.user.username
    template = loader.get_template('account/your_ads.html')
    context = {
        'ads_list': get_ads_by_username(username),
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('account/profile.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))
