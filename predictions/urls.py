from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('predict/result/<int:prediction_id>/', views.prediction_result_view, name='prediction_result'),
    path('predict/batch/', views.batch_predict_view, name='batch_predict'),
    path('predict/batch/download/<int:batch_id>/', views.download_batch_csv_view, name='download_batch_csv'),
    path('history/', views.history_view, name='history'),
    path('history/export/', views.export_history_csv_view, name='export_history_csv'),
    path('prediction/<int:prediction_id>/', views.prediction_detail_view, name='prediction_detail'),
    path('model-performance/', views.model_performance_view, name='model_performance'),
]
