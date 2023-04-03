from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, ChoiceField
from unicodedata import decimal
from .choices import STATE_CHOICES


class Profile(models.Model):
    USERNAME_FIELD='email'
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.CharField(max_length=50, primary_key=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=25, blank=False, null=True)
    address1 = models.CharField(max_length=100, blank=False, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    state = models.CharField(max_length=2, blank=False, null=True, choices = STATE_CHOICES)
    zipcode = models.CharField(max_length=10, blank=False, null=True)


class FuelQuote(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    gallons_requested = models.DecimalField(max_digits = 6, decimal_places = 2)
    delivered_to = models.CharField(max_length= 200 )
    suggested_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 10, decimal_places= 2)

    def get_delivery_address(self):
        profile = self.user.profile
        address_components = [profile.address, profile.city, profile.state, profile.zipcode]
        return ", ".join(filter(None, address_components))


class pricing(models.Model):
    user_state = models.CharField(max_length = 2)
    rate_per_gallon = models.DecimalField(max_digits = 5, decimal_places= 2)
    profit_margin = models.DecimalField(max_digits = 5, decimal_places = 2)
    #pricing module