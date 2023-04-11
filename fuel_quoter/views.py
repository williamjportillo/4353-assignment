from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FuelQuoteForm, ManageProfileForm
from .models import FuelQuote
import sys
from django.utils.html import escape
from django.http import HttpResponse

class HomeView(View):

    template_name = 'base.html'
    form_class = FuelQuoteForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        fuel_quote = self.form_class(request.POST)
        data = request.POST
        user = request.user

        if not fuel_quote.is_valid():
            messages.error(request, 'Invalid input.')
            return render(request, self.template_name, context={'form': fuel_quote})
        elif not all([user.address1, user.city, user.state, user.zipcode]):
            messages.error(request, 'User must first complete their profile.')
            return render(request, self.template_name, context={'form': fuel_quote})

        fuel_quote = fuel_quote.save(commit=False)
        fuel_quote.user_id = user.id
        fuel_quote.gallons_requested = data.get('gallons_requested')
        fuel_quote.delivery_date = data.get('delivery_date')
        fuel_quote.address1 = user.address1
        fuel_quote.address2 = user.address2
        fuel_quote.city = user.city
        fuel_quote.state = user.state
        fuel_quote.zipcode = user.zipcode
        fuel_quote.price_rate = 2.54
        fuel_quote.total_due = round(float(fuel_quote.gallons_requested) * float(fuel_quote.price_rate), 2)
        fuel_quote.save()
        print(fuel_quote.id)
        #query_result = get_object_or_404(FuelQuote, id=fuel_quote.id)
        return redirect('quote/{}'.format(fuel_quote.id))


class QuoteView(View):
    
    template_name = 'quote.html'
    
    def get(self, request, quote_id):
        query_result = get_object_or_404(FuelQuote, id=quote_id)
        return render(request, self.template_name, context={'fuel_quote': query_result})

 
class QuoteHistoryView(View):
    
    template_name = 'quote_history.html'
    
    def get(self, request):
        fuel_quotes = FuelQuote.objects.filter(user_id=request.user.id).order_by('delivery_date')
        return render(request, self.template_name, context={'fuel_quotes': fuel_quotes})



class ManageProfileView(View):

    template_name = 'profile.html'
    form_class = ManageProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if not form.is_valid():
            messages.error(request, 'Invalid input.')
        else:
            form.save()
            messages.success(request, 'Your profile has updated successfully!')
        return render(request, self.template_name, context={'form': form})

