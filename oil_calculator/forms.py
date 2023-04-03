from dataclasses import fields
from datetime import datetime
from distutils.command.clean import clean
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
import zipapp
import zipfile
import zipimport
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password, check_password
from .models import Profile
from .choices import STATE_CHOICES
from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True, validators= [EmailValidator()])
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailField(max_length= 50, validators = [EmailValidator()]),
            'password': forms.CharField(widget = forms.PasswordInput)
        }

    """def clean(self):
        super(RegisterForm, self).clean()
        for field, data in self.cleaned_data:
            if len(data) > data.max_length:
                self._errors[field] = self.error_class(['Cannot exceed length of {}'.format(data.max_length)])
            if len(data) < data.min_length:
                self._errors[field] = self.error_class(['Minimum {} characters required'.format(data.min_length)])
        validation_regexs = {
            'email': '[a-zA-Z0-9]'
        }
        email=self.cleaned_data"""
    #def validate():
        #self._errors['password'] = self.validate

class ManageProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Profile
        fields = ['first_name', 'last_name', 'address1', 'address2', 'city',  'state', 'zipcode']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'address1': forms.TextInput(attrs={'required': True}),
            'address2': forms.TextInput(),
            'city': forms.TextInput(attrs={'required': True}),
            'state': forms.TextInput(attrs={'choices': STATE_CHOICES, 'required': True}),
            'zipcode': forms.TextInput(attrs={'required': True})
        }

        def clean(self):
            cleaned_data = super().clean()
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            address1 = cleaned_data.get('address1')
            address2 = cleaned_data.get('address2')
            city = cleaned_data.get('city')
            zippcode = cleaned_data.get('zipcode')


            if not first_name.isalpha():
                raise forms.ValidationError('First name should only contain letters')
            if not last_name.isalpha():
                raise forms.ValidationError('Last name should only contain letters')
            if not address1.isalnum():
                raise forms.ValidationError('Address should not contain any symbols')
            if not address2.isalnum():
                raise forms.ValidationError('Address should not contain any symbols')
            if not city.isalpha():
                raise forms.ValidationError('City should only contain letters')
            if not zipcode.isdigit():
                raise forms.ValidationError('Zip should only contain numbers')

            return cleaned_data

    """def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address1 = self.cleaned_data['address1']
        user.address2 = self.cleaned_data['address2']
        user.city = self.cleaned_data['city']
        user.state = self.cleaned_data['state']
        user.zipcode = self.cleaned_data['zipcode']
        if commit:
            user.save()
        return user"""

class QuoteRequestForm(forms.Form):
    gallons_requested = forms.DecimalField(max_digits=7, decimal_places=2, label='Gallons Requested')
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Delivery Date')

    def clean(self):
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        gallons_requested  = cleaned_data.get('gallons_requested')

        if date < datetime.date.today():
            raise forms.ValidationError("Date cannot be in the past")
        if gallons_requested <= 0:
            raise forms.ValidationError("Enter a positive number")
