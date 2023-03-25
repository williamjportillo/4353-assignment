"""
oil_calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
#from django.contrib import admin
from cgitb import html
import profile
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

urlpatterns = [
    # Uncomment the next line to enable the admin:
    #path('admin/', admin.site.urls)
    path('', views.home, name = 'oil_calculator'),
    path('profile/', views.profile, name = 'profile'),
    path('quote_history/', views.quote_history, name = 'quote_history'),
    path('login/', auth_views.LoginView.as_view(template_name = 'empty.html', authentication_form = AuthenticationForm), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(),name = 'logout')
]