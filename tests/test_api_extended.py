import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from predictions.models import ModelInformation

@pytest.mark.django_db
def test_api_model_performance_endpoint():
    client = APIClient()
    ModelInformation.objects.create(
        model_name="Test Model",
        algorithm="Logistic Regression",
        version="1.0.0",
        accuracy=0.80,
        precision=0.75,
        recall=0.70,
        f1_score=0.72,
        roc_auc=0.78,
        is_active=True
    )
    url = reverse('api_model_performance')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]['algorithm'] == "Logistic Regression"

@pytest.mark.django_db
def test_api_dashboard_stats_endpoint():
    client = APIClient()
    user = User.objects.create_user(username='dashuser', password='password123')
    client.force_authenticate(user=user)
    
    url = reverse('api_dashboard_stats')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'total_predictions' in response.data
    assert 'average_probability' in response.data
