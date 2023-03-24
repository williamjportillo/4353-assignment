from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class login_form(UserCreationForm):
    #login form


class register_form(UserCreationForm):
    #user registration form

class manage_profile_form(UserCreationForm):
    #user profile form

class calculator_form(UserCreationForm):
    #price estimator form
