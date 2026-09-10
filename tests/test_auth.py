from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTests(TestCase):
    def test_user_registration(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'testanalyst',
            'email': 'analyst@bank.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testanalyst').exists())

    def test_user_login(self):
        User.objects.create_user(username='loginuser', email='login@bank.com', password='password123')
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'loginuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
