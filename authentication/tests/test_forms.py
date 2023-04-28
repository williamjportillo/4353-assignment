from django.test import TestCase
from ..models import User
from ..forms import SignUpForm
from copy import copy

class FormTest(TestCase):

    def test_valid_user_creation_form(self):
        valid_form_data = {'email': 'unittest@email.com'}
        form = SignUpForm(data=valid_form_data)
        self.assertTrue(not form.is_valid())

    def test_invalid_user_creation_forms(self):
        valid_form_data = {'email': 'unittest@email.com', 'password': 'PassTest12!'}
        invalid_data = {
            'email': ['', 'test', 'test2@' 'a.com', 'test@email', 'test2@email', 'a'*45+'@b.net'],
            'password': ['', 'abcdef', '123405']
        }
        for field in invalid_data:
            invalid_form_data = valid_form_data.copy()
            for value in invalid_data[field]:
                invalid_form_data[field] = value
                form = SignUpForm(data=valid_form_data)
                self.assertFalse(form.is_valid())

    """def test_valid_user_creation_form(self):
        valid_form_data = {'email': 'unittest@email.com', 'first_name': 'Joe', 'last_name': 'Johnson', 'address1': '1500 El Camino', 'address2': 'Village Dr', 'city': 'Houston', 'state': 'TX', 'zipcode': '77504'}
        form = SignUpForm(data=valid_form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_creation_forms(self):
        valid_form_data = {'email': 'unittest@email.com', 'first_name': 'Joe', 'last_name': 'Johnson', 'address1': '1500 El Camino', 'address2': 'Village Dr', 'city': 'Houston', 'state': 'TX', 'zipcode': '77504'}
        invalid_data = {
            'email': ['', 'test', 'test2@' 'a.com', 'test@email', 'test2@email', 'a'*45+'@b.net'],
            'first_name': ['', 'a'*26],
            'last_name': ['', 'a'*26],
            'address1': ['', 'a'*101],
            'address2': ['a'*101],
            'city': ['', 'a'*51],
            'state': ['', 'A', 'PQ', 'TXB', 'tx'],
            'zipcode': ['', '1234567890', 'abcde', '123456', '1'],
        }
        for field in invalid_data:
            invalid_form_data = valid_form_data.copy()
            for value in invalid_data[field]:
                invalid_form_data[field] = value
                form = SignUpForm(data=valid_form_data)
                self.assertFalse(form.is_valid())"""