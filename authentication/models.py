from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from .static.choices import STATE_CODES
# Create your models here.

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator])
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=25, blank=False, null=True)
    address1 = models.CharField(max_length=100, blank=False, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    state = models.CharField(max_length=2, blank=False, null=True, choices = STATE_CODES)
    zipcode = models.CharField(max_length=10, blank=False, null=True)

