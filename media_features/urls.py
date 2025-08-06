# media_features/urls.py (This is the one in your media_features app folder)

from django.urls import path
from . import views



urlpatterns = [
    # New: This is the URL for the main dashboard listing all forms
    path('', views.reports_dashboard, name='reports_dashboard'),

    
    path('table-10-media-features/', views.media_feature_form, name='table_10_form'),
    path('table-11-technologies/', views.technology_commercialized_form, name='table_11_form'),

    # New: This is the centralized URL for the multi-sheet Excel export
    path('export-all/', views.export_all_to_excel, name='export_all_to_excel'),
    path('get-curricular-offerings/<int:department_id>/', views.get_curricular_offerings, name='get_curricular_offerings'),
    
    
]

