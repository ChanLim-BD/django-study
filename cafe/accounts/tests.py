from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_with_valid_credentials(self):
        data = {
            'phone': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.signup_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['meta']['code'], 201)

    def test_signup_with_existing_phone(self):
        User.objects.create_user(username='1234567890', password='testpassword')
        data = {
            'phone': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.signup_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['meta']['code'], 400)
        self.assertEqual(response.json()['meta']['message'], 'PHONE_DUPLICATED')

    def test_signup_with_missing_fields(self):
        data = {
            'phone': '',
            'password': ''
        }
        response = self.client.post(self.signup_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['meta']['code'], 400)
        self.assertEqual(response.json()['meta']['message'], 'Enter Your User Phone or Password')


class SignInViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('signin')

    def test_signin_with_valid_credentials(self):
        user = User.objects.create_user(username='1234567890', password='testpassword')
        data = {
            'phone': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.signin_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['meta']['code'], 200)
        self.assertEqual(response.wsgi_request.user, user)

    def test_signin_with_invalid_credentials(self):
        data = {
            'phone': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(self.signin_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['meta']['code'], 401)
        self.assertIsNone(response.wsgi_request.user)

    def test_signin_with_missing_fields(self):
        data = {
            'phone': '',
            'password': ''
        }
        response = self.client.post(self.signin_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['meta']['code'], 400)
        self.assertEqual(response.json()['meta']['message'], 'Enter Your User Phone or Password')


class SignOutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signout_url = reverse('signout')

    def test_signout(self):
        self.client.login(username='1234567890', password='testpassword')
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['MESSAGE'], 'SUCCESS')
        self.assertIsNone(response.wsgi_request.user)
