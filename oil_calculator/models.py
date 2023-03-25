django.db from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, ChoiceField
from choices import STATE_CHOICES




class login(models.model):
    #login module; in
    
class profile(models.model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_address1 = models.CharField(max_length = 100, blank = False, null = False)
    user_address2 = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50, blank = False, null = False)
    state = models.CharField(max_length= 2, choices = STATE_CHOICES, blank = False, null = False)
    zipcode = models.CharField(max_length = 9, blank = False, null = False)



class fuel_quote(models.model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    gallons_requested = models.DecimalField(max_digits = 6, decimal_places = 2)
    delivered_to = models.CharField(max_length= 200 )
    suggested_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 10, decimal_places= 2)

    def get_delivery_address(self):
        profile = self.user.profile
        address_components = [profile.address, profile.city, profile.state, profile.zipcode]
        return ", ".join(filter(None, address_components))


class pricing(models.model):
    user_state = models.CharField(max_length = 2)
    rate_per_gallon = models.DecimalField(max_digits = 5, decimal_places= 2)
    profit_margin = models.DecimalField(max_digits = 5, decimal_places = 2)
    #pricing module