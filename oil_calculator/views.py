from django.shortcuts import render

def home(request):
    return render(request, 'oil_calculator.html')

def profile(request):
    return render(request, 'profile.html')


def quote_history(request):
    return render(request, 'quote_history.html')
