from django.test import TestCase
from django.urls import reverse
from .forms import FuelQuoteForm
from authentication.tests.test_models import ModelTest
from authentication.models import User
from django.test.client import Client

# Create your tests here.
class ViewTest(TestCase):
    
    def test_home_view(self):
        password = 'PassTest12!' 
        self.user = User.objects.create(email='myemail@test.com', password=password)
        self.client.login(email=self.user.email, password=password)
        url = reverse('home')
        resp = self.client.get(url, data={'gallons_requested': 1000, 'delivery_date': '2023-04-23'})
        self.assertEqual(resp.status_code, 302)