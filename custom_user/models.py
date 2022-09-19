from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
  username = None
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  phone = models.CharField(max_length=20, blank=True)
  TYPES = (
    ('User','User'),
    ('Driver','Driver'),
    ('Admin','Admin'),
  )
  types = models.CharField(max_length = 10, null=True,choices=TYPES)
  address = models.CharField(max_length=200, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ( 'first_name', 'last_name', 'phone', 'types')
  # REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.email