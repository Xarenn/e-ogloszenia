from django.contrib import admin

from core.models import Ad
from security.models import User

admin.site.register(User)
admin.site.register(Ad)
