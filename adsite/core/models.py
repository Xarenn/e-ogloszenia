from django.db import models
from security.models import User

class Ad(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    bump_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='/images', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
    