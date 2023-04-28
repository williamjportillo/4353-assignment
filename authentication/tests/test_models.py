from django.test import TestCase
from ..models import User
from django.urls import reverse

# Create your tests here.
class ModelTest(TestCase):

    def create_user(self, email='unittest@email.com', first_name='Joe', last_name='Johnson', address1='1500 El Camino', address2='Village Dr', city='Houston', state='TX', zipcode='77509'):
        return User.objects.create(email=email, first_name=first_name, last_name=last_name, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode)

    def delete_user(self, email):
        return User.objects.filter(email=email).delete()

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))

    def test_user_deletion(self):
        user = self.create_user()
        self.delete_user(user.email)
        self.assertTrue(not list(User.objects.filter(email=user.email)))

    """def test_login_view(self):
        url = reverse('login')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)"""