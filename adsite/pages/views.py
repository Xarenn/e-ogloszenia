from django.shortcuts import render
from django.core.paginator import Paginator
import requests as r

def home_view(request, *args, **kwargs):
    
    paginator = Paginator(fake_ads, 20)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    return render(request, 'index.html', {'ads': ads})


def ad_detail_view(request, *args, **kwargs):
    ad_id = request.GET.get('id')
    response = r.get(f'http://localhost:8080/system/ads/{ad_id}')
    ad = response.json()
    return render(request, 'ad_detail_view.html', ad)



def _create_fake_ad():
    fake = AdFake()
    fake.title = "JEBAC PIS"
    fake.shortDescription = "shortdesc"
    fake.price = 12
    fake.phone = "12321312"
    fake.description = "Konferedacja Konfederacja to jest jedna racja"
    fake.featured = True
    fake.id = 1
    return fake
