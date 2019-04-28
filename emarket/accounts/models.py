from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    chats = models.ManyToManyField('Chat')


class Chat(models.Model):
    title = models.TextField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Message(models.Model):
    body_text = models.TextField(max_length=1255, default="")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Ad(models.Model):
    title = models.TextField(max_length=125)
    short_description = models.TextField(max_length=300, default="")
    description = models.TextField(max_length=9000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
