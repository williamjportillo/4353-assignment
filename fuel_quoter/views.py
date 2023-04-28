from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .forms import FuelQuoteForm, ManageProfileForm
from .models import FuelQuote


class HomeView(View):
    template_name = 'base.html'
    form_class = FuelQuoteForm

    def get(self, request):
        form = self.form_class()
        if not request.user.is_authenticated:
            return redirect('login')
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

        request.session['fuel_quote_user_id'] = user.id
        request.session['fuel_quote_gallons_requested'] = format(float(data.get('gallons_requested')), ',.2f')
        request.session['fuel_quote_delivery_date'] = data.get('delivery_date')
        request.session['fuel_quote_address1'] = user.address1
        request.session['fuel_quote_address2'] = user.address2
        request.session['fuel_quote_city'] = user.city
        request.session['fuel_quote_state'] = user.state
        request.session['fuel_quote_zipcode'] = user.zipcode

        margin = 0.1
        margin += .02 if user.state == 'TX' else .04
        margin += .02 if float(data.get('gallons_requested')) > 1000 else .03
        margin -= .01 if FuelQuote.objects.filter(user_id=user.id) else 0
        price_rate = 1.5 * (1 + margin)
        total_due = float(data.get('gallons_requested')) * price_rate
        request.session['fuel_quote_price_rate'] = format(price_rate, ',.2f')
        request.session['fuel_quote_total_due'] = format(total_due, ',.2f')

        return redirect('quote')


class QuoteView(View):
    template_name = 'quote.html'
    form_class = FuelQuoteForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        fuel_quote = self.form_class()
        fuel_quote = fuel_quote.save(commit=False)
        fuel_quote.user_id = request.session['fuel_quote_user_id']
        fuel_quote.gallons_requested = float(request.session['fuel_quote_gallons_requested'].replace(',', ''))
        fuel_quote.delivery_date = request.session['fuel_quote_delivery_date']
        fuel_quote.address1 = request.session['fuel_quote_address1']
        fuel_quote.address2 = request.session['fuel_quote_address2']
        fuel_quote.city = request.session['fuel_quote_city']
        fuel_quote.state = request.session['fuel_quote_state']
        fuel_quote.zipcode = request.session['fuel_quote_zipcode']
        fuel_quote.price_rate = float(request.session['fuel_quote_price_rate'].replace(',', ''))
        fuel_quote.total_due = float(request.session['fuel_quote_total_due'].replace(',', ''))
        fuel_quote.save()
        return redirect('quote_history')


class QuoteHistoryView(View):
    template_name = 'quote_history.html'

    def get(self, request):
        fuel_quotes = FuelQuote.objects.filter(user_id=request.user.id).order_by('delivery_date')
        for fuel_quote in fuel_quotes:
            fuel_quote.gallons_requested = format(fuel_quote.gallons_requested, ',.2f')
            fuel_quote.price_rate = format(fuel_quote.price_rate, ',.2f')
            fuel_quote.total_due = format(fuel_quote.total_due, ',.2f')
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
