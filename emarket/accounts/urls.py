from django.urls import path

from . import views


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/add_ad/', views.add_ad, name='add_ad'),
    path('', views.ads_view, name='home'),
]
