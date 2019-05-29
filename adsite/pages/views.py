from django.shortcuts import render
from django.core.paginator import Paginator
import requests as r
from .api import get_ad_by_id

def home_view(request, *args, **kwargs):
    ads = ''
    return render(request, 'index.html', {'ads': ads})


def ad_detail_view(request, ad_id):
    response = r.get(get_ad_by_id + str(ad_id))
    ad = response.json()
    return render(request, 'ad_detail_view.html', ad)
