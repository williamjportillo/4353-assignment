from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
def home(request):
    return render(request, 'oil_calculator.html')

def profile(request):
    return render(request, 'profile.html')


def quote_history(request):
    return render(request, 'quote_history.html')

def login_popup(request):
    form = AuthenticationForm()
    return render(request, 'oil_caluclator.html', {'form' : form})