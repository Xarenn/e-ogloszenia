from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
