from django.contrib import admin
from django.urls import path, include, re_path
from pages import views
from security.views import register_view, change_password, show_details, edit_details, activate

urlpatterns = [
    path('', views.home_view, name='base'),
    path('home/', views.home_view, name='home'),
    path('search', views.search, name='search'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('account/change_password/', change_password, name='change_password'),
    path('details/', show_details, name='show_details'),
    path('edit_details/', edit_details, name='edit_details'),
    path('account/', include('django.contrib.auth.urls')),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
    path('ad/<int:ad_id>', views.ad_detail_view, name='ad_details'),
    path('account/my_ads', views.get_user_ads, name='user_ads'),
    path('account/create_ad', views.create_ad, name='create_ad'),
    path('account/edit_ad/<int:ad_id>', views.edit_ad, name='edit_ad'),
    path('error400', views.error_404, name='error404'),
]
