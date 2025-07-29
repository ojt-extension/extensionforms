# media_features/urls.py (This is the one in your media_features app folder)

from django.urls import path
from . import views

urlpatterns = [
    # URL for the main form and display page
    path('', views.media_feature_form, name='media_feature_form'),
    # URL for exporting data to CSV
    path('export-csv/', views.export_media_features_csv, name='export_media_features_csv'),
]
