
from django.contrib import admin
from django.urls import path, include
from pages import views
from security.views import register_view, change_password, show_details, edit_details

urlpatterns = [
    path('', views.home_view),
    path('home/', views.home_view, name='home'),
    path('register/', register_view, name='register'),
    path('admin/', admin.site.urls),
    path('account/change_password/', change_password, name='change_password'),
    path('details/', show_details, name='show_details'),
    path('edit_details/', edit_details, name='edit_details'),
    path('account/', include('django.contrib.auth.urls')),
]
