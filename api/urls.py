from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.api_register, name='api_register'),
    path('auth/login/', views.api_login, name='api_login'),
    path('predict/', views.api_predict, name='api_predict'),
    path('predictions/', views.api_predictions_list, name='api_predictions_list'),
    path('predictions/<int:prediction_id>/', views.api_prediction_detail, name='api_prediction_detail'),
    path('predictions/<int:prediction_id>/feedback/', views.api_prediction_feedback, name='api_prediction_feedback'),
    path('dashboard/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('model-performance/', views.api_model_performance, name='api_model_performance'),
]
