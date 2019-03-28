from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('account/add_ad/', views.add_ad, name='add_ad'),
    path('account/profile', views.profile, name='profile'),
    path('account/ads', views.your_ads, name='your_ads'),
    path('', views.ads_view, name='home'),
    path('search', views.search, name='search'),
    path('success_register', views.success_signup, name='success_register'),
    url(r'^ads/(?P<ad_id>\d+)$', views.ad_view, name='ad_view')
]
