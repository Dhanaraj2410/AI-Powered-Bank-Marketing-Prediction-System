from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='predictions')
    prediction_result = models.CharField(max_length=10)  # 'yes' or 'no'
    probability = models.FloatField()  # percentage e.g. 78.5
    confidence_level = models.CharField(max_length=50, default='High Confidence')
    risk_level = models.CharField(max_length=50, default='Low Risk Target')
    recommendation = models.TextField(blank=True, null=True)
    xai_factors_json = models.JSONField(default=dict, blank=True)
    feedback = models.CharField(max_length=10, blank=True, null=True)  # 'yes' or 'no'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Prediction #{self.id}: {self.prediction_result.upper()} ({self.probability}%)"

class BatchPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batch_predictions')
    file_name = models.CharField(max_length=255)
    total_records = models.IntegerField(default=0)
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    avg_probability = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Batch #{self.id} ({self.file_name}) - {self.total_records} rows"

class ModelInformation(models.Model):
    model_name = models.CharField(max_length=100)
    algorithm = models.CharField(max_length=100)
    version = models.CharField(max_length=20, default='1.0.0')
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    roc_auc = models.FloatField()
    confusion_matrix_json = models.JSONField(default=list)
    roc_curve_json = models.JSONField(default=dict)
    num_features = models.IntegerField(default=19)
    is_active = models.BooleanField(default=True)
    training_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.algorithm} (v{self.version}) - Acc: {self.accuracy*100:.1f}%"
