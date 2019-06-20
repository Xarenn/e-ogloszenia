from django.db import models
from security.models import User


class Ad(models.Model):

    TRUE = 'T'
    FALSE = 'F'
    ACTIVE_MODELS = (
        (TRUE, 'T'),
        (FALSE, 'F')
    )

    image = models.ImageField(upload_to = 'upload/', blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.CharField(choices=ACTIVE_MODELS, max_length=1, default=FALSE)
    server_id = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, verbose_name='Is Fetaured')
