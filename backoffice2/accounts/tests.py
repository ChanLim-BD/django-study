from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm


class CustomUserTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }

    def test_create_user(self):
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.status, 'W')

    def test_create_superuser(self):
        CustomUser = get_user_model()
        admin_user = CustomUser.objects.create_superuser(**self.user_data)
        self.assertEqual(admin_user.email, self.user_data['email'])
        self.assertTrue(admin_user.check_password(self.user_data['password']))
        self.assertEqual(admin_user.is_superuser, True)


class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_form_with_invalid_email(self):
        self.form_data['email'] = 'invalid-email'
        form = CustomUserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_with_different_passwords(self):
        self.form_data['password2'] = 'differentpassword'
        form = CustomUserCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
