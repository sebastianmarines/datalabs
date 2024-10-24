from django.urls import path
from .views import (
    DatasetListView,
    DatasetDetailView,
    DatasetCreateView,
)

app_name = 'dataset'

urlpatterns = [
    path('', DatasetListView.as_view(), name='dataset_list'),
    path('create/', DatasetCreateView.as_view(), name='dataset_create'),
    path('<int:pk>/', DatasetDetailView.as_view(), name='dataset_detail'),
]