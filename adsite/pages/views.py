from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core import static_data
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from core.forms.create_ad_form import AdForm
from core.forms.search_form import SearchFrom
from datetime import datetime

from core.models import Ad
from core.services.client_service import request_get, request_post
from pages.converter.json_converter import convert_json_to_ad, convert_form_to_ad
from security.auth import api_urls as api


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('server_id', 'title', 'description', 'image')


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

    assert (page is not None)
    json_dict = request_get(api.GET_ADS + f'page={page}&size=12')
    if json_dict is None:
        return render(request, 'index.html', {'ads': None, 'details': None, 'search_categories': static_data.categories})
    total_pages = json_dict.json()['totalPages']
    if page > total_pages - 1:
        json_dict = request_get(api.GET_ADS + f'page={total_pages - 1}&size=12')
    ads = json_dict.json()['content']
    details = _get_details(json_dict.json())
    return render(request, 'index.html', {'ads': ads, 'details': details})


def search(request):
    query = request.GET.get('q')
    ads_filtered = Ad.objects.filter(Q(title__icontains=query))
    paginator = Paginator(ads_filtered, 12)
    page_number_string = request.GET.get('page')

    try:
        page_number = int(page_number_string)
        if page_number <= 0:
            ads = paginator.get_page(1)
        elif page_number > paginator.num_pages:
            ads = paginator.get_page(paginator.num_pages)
        else:
            ads = paginator.get_page(page_number_string)

    except (TypeError, ValueError, KeyError):
        ads = paginator.get_page(1)
        return render(request, 'search_ads.html', {'ads': ads, 'query': query})

    return render(request, 'search_ads.html', {'ads': ads, 'query': query})


def ad_detail_view(request, ad_id):
    if not str(ad_id).isdigit():
        return render(request, 'index.html')
    ad = request_get(api.GET_AD_BY_ID + str(ad_id))
    if ad is None:
        return render(request, 'index.html')
    ad_db = Ad.objects.get(server_id=ad.json().get('id'))
    serializer = AdSerializer(ad_db)
    url_image = "http://localhost:8000"+ad_db.image.url
    return render(request, 'ad_detail_view.html', {'miniature': url_image, 'data': serializer.data})


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
            ad_db = get_object_or_404(Ad, server_id=ad_id)
            ad = _prepare_update_ad(request, ad_id, form)

            if ad_db.user.email != request.user.email:
                return error_404(request)

            response = request_post(api.UPDATE_AD_IN_USER, data=ad)

            if response is not None and response.status_code != 200:
                return redirect('user_ads')

            content = response.json()

            #   OTHER METHOD
            ad_db.server_id = content.get('id')
            ad_db.is_featured = content.get('featured', False)
            ad_db.description = content.get('description')
            ad_db.short_description = content.get('short_description')
            ad_db.title = content.get('title')
            ad_db.category = content.get('category')
            ad_db.personality = content.get('personality')
            ad_db.price = content.get('price')
            ad_db.is_active = Ad.FALSE
            ad_db.user = request.user
            Ad.save(ad_db)
            # TODO ad.image
            # TODO return valid html with success creating
        else:
            print("failed")

    else:
        ad_data = request_get(api.GET_AD_BY_ID + str(ad_id))
        ad_db = get_object_or_404(Ad, server_id=ad_id)
        if ad_db.user.email != request.user.email:
            return error_404(request)
        if ad_data.status_code != 200:
            return redirect("user_ads")

        form = AdForm(instance=convert_json_to_ad(ad_data.json()))
    return render(request, 'edit_ad.html', {'form': form})


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO OTHER METHOD
            ad_converted = convert_form_to_ad(form)
            ad_converted.user = request.user
            ad_converted.image = request.FILES['image']

            ad = _prepare_ad(request, form, ad_converted.image.url)
            response = request_post(api.CREATE_AD, data=ad)

            if response.status_code != 200:
                return redirect("user_ads")

            Ad.save(ad_converted)
            # TODO ad.image
            # TODO return valid html with success creating

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


def _prepare_update_ad(request, server_id, form):
    return {
        'login': request.user.email,
        'password': request.user.password,
        'AD_UPDATE_DTO': {
            'ad_server_id': server_id,
            'content_ad': _prepare_ad_dto(form)
        }

    }


def _prepare_ad(request, form, miniature_url):
    ad = {
        'login': request.user.email,
        'password': request.user.password,
        'AD': {
            'title': form.cleaned_data['title'],
            'phone': "23523523",
            'description': form.cleaned_data['description'],
            'category': form.cleaned_data['category'],
            'personality': form.cleaned_data['personality'],
            'price': form.cleaned_data['price'],
            'entry_date': datetime.now().isoformat(),
            'bump_date': datetime.now().isoformat(),
            'short_description': form.cleaned_data['short_description'],
            'featured': False,
            "photos": {
                "miniature_path": miniature_url,
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
        'title': form.cleaned_data['title'],
        'phone': '6666666',
        'description': form.cleaned_data['description'],
        'category': form.cleaned_data['category'],
        'personality': form.cleaned_data['personality'],
        'price': form.cleaned_data['price'],
        'entry_date': datetime.now().isoformat(),
        'bump_date': datetime.now().isoformat(),
        'short_description': form.cleaned_data['short_description'],
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
