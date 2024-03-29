from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from datetime import date

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False, verbose_name='staff account')
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )
    server_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    entry_date = models.DateField(default=date.today())
    phone = models.CharField(max_length=18)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    objects = UserManager()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
