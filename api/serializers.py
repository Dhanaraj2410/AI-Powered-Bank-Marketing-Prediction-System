from rest_framework import serializers
from django.contrib.auth.models import User
from customers.models import Customer
from predictions.models import Prediction, ModelInformation, BatchPrediction
from dataset_manager.models import DatasetInformation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Prediction
        fields = '__all__'

class ModelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelInformation
        fields = '__all__'

class PredictionInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(default=35)
    job = serializers.CharField(default='admin.')
    marital = serializers.CharField(default='married')
    education = serializers.CharField(default='university.degree')
    default = serializers.CharField(default='no')
    housing = serializers.CharField(default='yes')
    loan = serializers.CharField(default='no')
    contact = serializers.CharField(default='cellular')
    month = serializers.CharField(default='may')
    day_of_week = serializers.CharField(default='mon')
    campaign = serializers.IntegerField(default=1)
    pdays = serializers.IntegerField(default=999)
    previous = serializers.IntegerField(default=0)
    poutcome = serializers.CharField(default='nonexistent')
    emp_var_rate = serializers.FloatField(default=1.1)
    cons_price_idx = serializers.FloatField(default=93.994)
    cons_conf_idx = serializers.FloatField(default=-36.4)
    euribor3m = serializers.FloatField(default=4.857)
    nr_employed = serializers.FloatField(default=5191.0)
