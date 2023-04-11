from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import FuelQuote
from authentication.models import User
from .static.choices import STATE_CODES

def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )
    
def validate_min_gallons(value):
    if value < 10:
        raise ValidationError(
            _('Must request at least 10 gallons of fuel'),
            params={'value': value},
        )
    
def validate_max_gallons(value):
    if value > 1000:
        raise ValidationError(
            _('Cannot request more than 1000 gallons of fuel'),
            params={'value': value},
        )

fuel_validators = [validate_positive, validate_min_gallons, validate_max_gallons]

class FuelQuoteForm(forms.ModelForm):
    class Meta:
        model = FuelQuote
        fields = ['gallons_requested', 'delivery_date']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'})
        }

class ManageProfileForm(forms.ModelForm):
    email = None
    password = None
    first_name = forms.CharField(max_length=25, required=True)
    last_name = forms.CharField(max_length=25, required=True)
    address1 = forms.CharField(max_length=100, required=True)
    address2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=2, required=True)
    zipcode = forms.CharField(max_length=10, required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zipcode']
        widgets = {
            'state': forms.Select(attrs={'choices': STATE_CODES})
        }


        