from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from .models import Profile
from .choices import STATE_CHOICES


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
class RegisterForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(),
            'password': forms.PasswordInput()
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

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.hashed_password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ManageProfileForm(UserChangeForm):
    class Meta:
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