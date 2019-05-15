
from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('admin/', admin.site.urls),
]
