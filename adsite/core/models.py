from django.db import models
from django.urls import reverse

from core import static_data
from security.models import User


def location_file(instance, filename):
    return 'user_images/%s/%s' % (instance.server_id, filename)


class Ad(models.Model):

    TRUE = 'T'
    FALSE = 'F'
    ACTIVE_MODELS = (
        (TRUE, 'T'),
        (FALSE, 'F')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.CharField(
        choices=ACTIVE_MODELS, max_length=1, default=FALSE)
    server_id = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(
        default=False, verbose_name='Is Fetaured')
    title = models.CharField(default=None, max_length=255, null=False)
    category = models.CharField(default=None,
                                choices=static_data.categories, max_length=64, null=False)
    short_description = models.CharField(
        default=None, max_length=120, null=False)
    personality = models.CharField(
        default=None, choices=static_data.personality, max_length=64, null=False)
    description = models.TextField(default=None, max_length=1024, null=False)
    price = models.FloatField(default=0, null=False)
    image = models.ImageField(upload_to=location_file)
