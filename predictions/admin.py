from django.contrib import admin
from .models import Prediction, BatchPrediction, ModelInformation

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'prediction_result', 'probability', 'confidence_level', 'risk_level', 'created_at')
    list_filter = ('prediction_result', 'confidence_level', 'risk_level', 'created_at')
    search_fields = ('user__username', 'customer__job', 'prediction_result')

@admin.register(BatchPrediction)
class BatchPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_name', 'total_records', 'yes_count', 'no_count', 'avg_probability', 'created_at')
    list_filter = ('created_at',)

@admin.register(ModelInformation)
class ModelInformationAdmin(admin.ModelAdmin):
    list_display = ('algorithm', 'version', 'accuracy', 'precision', 'recall', 'f1_score', 'roc_auc', 'is_active', 'training_date')
    list_filter = ('is_active', 'algorithm')
