from django.db import models
from security.models import User

class Ad(models.Model):
    image = models.ImageField(upload_to = 'upload/', blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    