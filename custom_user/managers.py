from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password, first_name, last_name, phone, types, address,  **extra_fields):
    if not email:
      raise ValueError(_('The Email must be set'))
    email = self.normalize_email(email)
    phone = extra_fields.get('phone')
    first_name = extra_fields.get('first_name')
    last_name = extra_fields.get('last_name')
    types = extra_fields.get('types')
    user = self.model(email=email, phone=phone, first_name=first_name, last_name=last_name, types=types, address = address, **extra_fields)
    # user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError(_('Superuser must have is_staff=True.'))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_('Superuser must have is_superuser=True.'))
    return self.create_user(email, password, **extra_fields)