import pytest
from django.contrib.auth.models import User
from accounts.models import UserProfile
from customers.models import Customer
from predictions.models import Prediction, BatchPrediction, ModelInformation

@pytest.mark.django_db
def test_user_profile_creation():
    user = User.objects.create_user(username='testuser', password='password123')
    profile = UserProfile.objects.create(
        user=user,
        full_name='John Doe',
        address='123 Main St, New York, NY',
        phone='+1-555-0199',
        occupation='Financial Analyst'
    )
    assert profile.full_name == 'John Doe'
    assert profile.address == '123 Main St, New York, NY'
    assert str(profile) == "John Doe's Profile"

@pytest.mark.django_db
def test_customer_and_prediction_relationship():
    user = User.objects.create_user(username='analyst', password='password123')
    customer = Customer.objects.create(age=40, job='management', marital='married', education='university.degree')
    prediction = Prediction.objects.create(
        user=user,
        customer=customer,
        prediction_result='yes',
        probability=85.5,
        confidence_level='High Confidence',
        risk_level='Low Risk Target'
    )
    assert prediction.customer == customer
    assert prediction.user == user
    assert prediction.probability == 85.5
    assert str(prediction) == f"Prediction #{prediction.id}: YES (85.5%)"

