import profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ChoiceField
from .choices import STATE_CHOICES

class login_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class register_form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class manage_profile_form(UserCreationForm):
    class profileForm(ModelForm):
        state = ChoiceField(choices= STATE_CHOICES)
    class Meta:
        model = profile
        fields = ['user_address1', 'user_address2', 'city', 'state', 'zipcode']
        widgets = {
            'user_address1': forms.TextInput(attrs={'class': 'form-control'}),
            'user_address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
        }

class calculator_form(UserCreationForm):
    gallons_requested = forms.DecimalField(max_digits=7, decimal_places=2, label='Gallons Requested')
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Delivery Date')



