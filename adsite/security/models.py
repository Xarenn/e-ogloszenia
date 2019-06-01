from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from datetime import date

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )
    name = models.CharField(max_length=128)
    entry_date = models.DateField(default=date.today())
    phone = models.CharField(max_length=18)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    objects = UserManager()
