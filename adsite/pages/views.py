from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from core.create_ad_form import AdForm
import json
from datetime import datetime
from django.utils.timezone import now
import requests 
from security import api_urls as api
from core import static_data


def home_view(request, *args, **kwargs):
    page = kwargs['page']
    print(page)
    return render(request, 'index.html', {'ads': ads})


def ad_detail_view(request, ad_id):
    response = requests.get(api.GET_AD_BY_ID + str(ad_id))
    ad = response.json()
    return render(request, 'ad_detail_view.html', ad)


@login_required
def get_user_ads(request):
    return render(request, 'user_ads.html')


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = {}
            ad['login'] = request.user.email
            ad['password'] = request.user.password
            form_data = form.cleaned_data
            ad['AD'] = {
                **form_data,
                **static_data.details,
            }
            request_data = json.dumps(ad)
            requests.post(api.CREATE_AD, json=request_data)
    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})
