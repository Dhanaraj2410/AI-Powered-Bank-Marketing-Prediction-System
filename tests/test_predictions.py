from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from predictions.models import Prediction

class PredictionTests(TestCase):
    def test_prediction_creation(self):
        user = User.objects.create_user(username='preduser', password='password123')
        self.client.force_login(user)

        url = reverse('predict')
        response = self.client.post(url, {
            'age': 38,
            'job': 'admin.',
            'marital': 'married',
            'education': 'university.degree',
            'default': 'no',
            'housing': 'yes',
            'loan': 'no',
            'contact': 'cellular',
            'month': 'may',
            'day_of_week': 'mon',
            'campaign': 1,
            'previous': 0,
            'poutcome': 'nonexistent'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Prediction.objects.filter(user=user).count(), 1)
