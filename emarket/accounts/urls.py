from django.urls import path

from . import views


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/add_ad/', views.add_ad, name='add_ad'),
    path('accounts/profile', views.your_ads, name='your_ads'),
    path('', views.ads_view, name='home'),
    path('success_register', views.success_signup, name='success_register')
]
