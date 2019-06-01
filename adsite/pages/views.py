from django.shortcuts import render
from django.core.paginator import Paginator
import requests as r
from . import api
from django.contrib.auth.decorators import login_required
from core.create_ad_form import AdForm
import json
from datetime import datetime
from django.utils.timezone import now
import requests as r
from security import api_urls as api


def home_view(request, *args, **kwargs):
    ads = ''
    return render(request, 'index.html', {'ads': ads})


def ad_detail_view(request, ad_id):
    response = r.get(api.GET_AD_BY_ID + str(ad_id))
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
                **_get_details(),
            }
            request_data = json.dumps(ad)
            r.post(api.CREATE_AD, json=request_data)
    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})


def _get_details():
    return {
        'featured': False,
        'entry_date': datetime.now().isoformat(),
        'bump_date':  datetime.now().isoformat(),
        "photos": {
            "miniature_path": "ad:miniature.jpg",
            "files_path": [
                "ad:FCI1.jpg",
                "ad:picture2.jpg",
                "ad:picture5.jpg"
            ]
        }
    }
