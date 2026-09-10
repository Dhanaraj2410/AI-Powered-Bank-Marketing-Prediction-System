from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class APIRestTests(APITestCase):
    def test_api_predict(self):
        user = User.objects.create_user(username='apiuser', password='password123')
        self.client.force_authenticate(user=user)

        url = '/api/predict/'
        response = self.client.post(url, {
            'age': 45,
            'job': 'management',
            'marital': 'married',
            'education': 'university.degree',
            'housing': 'yes',
            'loan': 'no',
            'contact': 'cellular',
            'campaign': 2
        }, format='json')

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('prediction', data)
        self.assertIn('probability', data)
        self.assertIn('xai_factors', data)
