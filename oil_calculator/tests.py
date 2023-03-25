from django.test import TestCase
from forms import *
from models import *
from django.urls
from django.urls import reverse

class loginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertRedirects(response, self.dashboard_url, status_code=302)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_dashboard_redirect_unauthenticated_user(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, self.login_url + '?next=' + self.dashboard_url, status_code=302)
class profileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = profile.objects.create(user=self.user, user_address1='123 Main St', city='Anytown', state='TX', zipcode='12345')

    def test_profile_creation(self):
        self.assertIsInstance(self.profile, profile)
        self.assertEqual(str(self.profile), self.user.username + ' Profile')

    def test_profile_attributes(self):
        self.assertEqual(self.profile.user_address1, '123 Main St')
        self.assertEqual(self.profile.city, 'Anytown')
        self.assertEqual(self.profile.state, 'TX')
        self.assertEqual(self.profile.zipcode, '12345')
class fuel_quoteTest(TestCase):
        def setUp(self):
        self.profile = profile.objects.create(
            user_address1="123 Main St",
            city="Houston",
            state="TX",
            zipcode="77001",
        )

    def test_create_fuel_quote(self):
        fuel_quote = fuel_quote.objects.create(
            profile=self.profile,
            gallons_requested=100,
            delivery_address=self.profile.get_full_address(),
            delivery_date="2023-04-01",
            suggested_price=2.5,
            total_amount_due=250,
        )

        self.assertEqual(fuel_quote.gallons_requested, 100)
        self.assertEqual(fuel_quote.delivery_address, self.profile.get_full_address())
        self.assertEqual(fuel_quote.delivery_date, "2023-04-01")
        self.assertEqual(fuel_quote.suggested_price, 2.5)
        self.assertEqual(fuel_quote.total_amount_due, 250)

class registrationFormTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
        }
    
    def test_register_user(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')
        
    def test_register_user_password_mismatch(self):
        self.user_data['password2'] = 'mismatchpass'
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertContains(response, 'The two password fields didn')
        self.assertEqual(User.objects.count(), 0)

class calculator_formTest(TestCase):
    def test_fuelquoteform_valid_data(self):
        form = calculator_form(data={
            'gallons_requested': '100',
            'delivery_date': date.today()
        })
        self.assertTrue(form.is_valid())
        
    def test_fuelquoteform_missing_data(self):
        form = calculator_form(data={
            'gallons_requested': '',
            'delivery_date': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
