from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm

def home(request):
    return render(request, 'oil_calculator.html')

def profile(request):
    return render(request, 'profile.html')

def quote_history(request):
    return render(request, 'quote_history.html')

def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

def login_view(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'], 
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})
        
def logout_view(request):
    pass
      