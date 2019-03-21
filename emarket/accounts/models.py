from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Ad(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField(max_length=9000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
