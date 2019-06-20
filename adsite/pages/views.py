from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms.create_ad_form import AdForm
from datetime import datetime

from core.models import Ad
from core.services.client_service import request_get, request_post
from security.auth import api_urls as api
from security.auth.api_urls import GET_AD_BY_ID


def home_view(request, *args, **kwargs):
    page_number = request.GET.get('page')
    page = 0
    if page_number is not None:
        try:
            page = int(page_number) - 1
            if page < 0:
                return redirect('/')
        except (TypeError, ValueError, KeyError):
            return redirect('/')
    assert(page is not None)
    json_dict = request_get(api.GET_ADS + f'page={page}&size=12')
    if json_dict is None:
        return render(request, 'index.html', {'ads': None, 'details': None})

    ads = json_dict.json()['content']
    details = _get_details(json_dict.json())
    return render(request, 'index.html', {'ads': ads, 'details': details})


def ad_detail_view(request, ad_id):
    if not str(ad_id).isdigit():
        return render(request, 'index.html')
    ad = request_get(api.GET_AD_BY_ID + str(ad_id))
    if ad is None:
        return render(request, 'index.html')
    return render(request, 'ad_detail_view.html', ad.json())


@login_required
def get_user_ads(request):
    email = request.user.email
    data = request_get(api.GET_ADS_BY_USER_EMAIL + email)

    if data is None or data.status_code != 200:
        return render(request, 'user_ads.html', {'ads': []})

    ads = data.json()
    return render(request, 'user_ads.html', {'ads': ads})


@login_required
def edit_ad(request, ad_id):
    if request.method == 'POST' and str(ad_id).isdigit():

        form = AdForm(request.POST)
        if form.is_valid():
            ad = _prepare_update_ad(request, server_id, form)
            response = request_post(api.UPDATE_AD_IN_USER, data=ad)

            if response is not None and response.status_code != 200:
                return get_user_ads(request)

            content = response.json()

            # TODO OTHER METHOD
            ad = Ad()
            ad.server_id = content.get('id', None)
            ad.is_featured = content.get('featured', None)
            ad.is_active = Ad.FALSE
            ad.user = request.user
            Ad.objects.filter(pk=ad_id).update(is_featured=content.get('featured', False))
            #TODO ad.image
            #TODO return valid html with success creating

    else:
        ad_data = request_get(api.GET_AD_BY_ID + _get_ad_server_id(ad_id))

        if ad_data.status_code != 200:
            return redirect("user_ads")

        form = AdForm(ad_data.json())
    return render(request, 'create_ad.html', {'form': form})


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = _prepare_ad(request, form)
            response = request_post(api.CREATE_AD, data=ad)
            content = response.json()

            # TODO OTHER METHOD
            ad = Ad()
            ad.server_id = content.get('id', None)
            ad.is_featured = content.get('featured', None)
            ad.is_active = Ad.FALSE
            ad.user = request.user
            Ad.save(ad)
            #TODO ad.image
            #TODO return valid html with success creating

    else:
        form = AdForm()
    return render(request, 'create_ad.html', {'form': form})


def error_404(request):
    return render(request, 'error_404.html')


def _get_details(json_dict):
    return {
        'first': json_dict['first'],
        'last': json_dict['last'],
        'number': json_dict['number'] + 1
    }


def _prepare_update_ad(request, ad, form):
    return {
        'login': request.user.email,
        'password': request.user.password,
        'AD_UPDATE_DTO': {
            'ad_server_id': ad.server_id,
            'content_ad': _prepare_ad_dto(form)
        }

    }


def _prepare_ad(request, form):
    ad = {
        'login': request.user.email,
        'password': request.user.password,
        'AD': {
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
    }
    return ad


def _prepare_ad_dto(form):
    return {
        'AD': {
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
    }


def _get_ad_server_id(ad_id):
    return Ad.objects.all().filter(id=ad_id)
