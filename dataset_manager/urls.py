from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.dataset_list_view, name='dataset_list'),
    path('upload/', views.upload_dataset_view, name='upload_dataset'),
]
