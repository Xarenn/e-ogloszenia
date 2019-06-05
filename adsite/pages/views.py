from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from core.create_ad_form import AdForm
import json
from datetime import datetime
from django.utils.timezone import now
import requests
from security import api_urls as api
from core import static_data
from pprint import pprint


def home_view(request, *args, **kwargs):
    page = request.GET.get('page')
    if page is None:
        json_dict = requests.get(api.GET_ADS + 'page=0&size=20').json()
    else:
        try:
            page = int(page) - 1
            if page < 0:
                return redirect('error400')
        except (ValueError, KeyError):
            return redirect('error400')
        json_dict = requests.get(api.GET_ADS + f'page={page}&size=20').json()
    ads = json_dict['content']
    details = _get_details(json_dict)
    total_pages = json_dict['totalPages']
    return render(request, 'index.html', {'ads': ads, 'details': details, 'range': range(1, total_pages+1)})


def ad_detail_view(request, ad_id):
    response = requests.get(api.GET_AD_BY_ID + str(ad_id))
    ad = response.json()
    return render(request, 'ad_detail_view.html', ad)


@login_required
def get_user_ads(request):
    email = request.user.email
    data = requests.get(api.GET_ADS_BY_USER_EMAIL + email)
    ads = data.json()
    return render(request, 'user_ads.html', {'ads': ads})
    

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = _prepare_ad(request, form)
            request_data = json.dumps(ad)
            response = requests.post(api.CREATE_AD, json=ad)
            print(request_data)
            print(response.content)
    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})


def error_400(request):
    return render(request, 'error_400.html')


def _get_details(json_dict):
    temp = {}
    temp['first'] = json_dict['first']
    temp['last'] = json_dict['last']
    temp['number'] = json_dict['number'] + 1
    return temp


def _prepare_ad(request, form):
    ad = {}
    ad['login'] = request.user.email
    ad['password'] = request.user.password
    ad['AD'] = {
        'title': form.cleaned_data['title'],
        'phone': '6666666',
        'description': form.cleaned_data['description'],
        'category': form.cleaned_data['category'],
        'personality': form.cleaned_data['personality'],
        'price': form.cleaned_data['price'],
        'entry_date': datetime.now().isoformat(),
        'bump_date':  datetime.now().isoformat(),
        'short_description':  form.cleaned_data['short_description'],
        'featured': False,
        "photos": {
            "miniature_path": "ad:miniature.jpg",
            "files_path": [
                "ad:FCI1.jpg",
                "ad:picture2.jpg",
                "ad:picture5.jpg"
            ]
        }
    }
    return ad
