from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm

def home(request):
    return render(request, 'oil_calculator.html')

def profile(request):
    return render(request, 'profile.html')

def quote_history(request):
    return render(request, 'quote_history.html')

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        #return render(request, request.view, {'form' : form})
        return render(request, 'oil_calculator.html', {'form' : form})

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        #return render(request, request.view, {'form' : form})
        return render(request, 'oil_calculator.html', {'form' : form})
    
def logout(request):
    pass