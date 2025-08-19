# media_features/urls.py (This is the one in your media_features app folder)

from django.urls import path
from . import views



urlpatterns = [
    #url for admin side view details:
    path('table-3-details/<int:submission_id>/', views.training_details, name='table_3_details'),
    path('table-8-details/<int:submission_id>/', views.faculty_involvement_details, name='table_8_details'),
    path('table-9-details/<int:submission_id>/', views.student_involvement_details, name='table_9_details'),
    path('table-10-details/<int:submission_id>/', views.media_features_details, name='table_10_details'),
    path('table-11-details/<int:submission_id>/', views.technologies_details, name='table_11_details'),

    # New: This is the URL for the main dashboard listing all forms
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('table-3-training/', views.training_form_view, name='table_3_form'),
    path('table-8-faculty-involvement/', views.faculty_involvement_form, name='table_8_form'),
    path('table-9-student-involvement/', views.student_involvement_form, name='table_9_form'),
    path('table-10-media-features/', views.media_feature_form, name='table_10_form'),
    path('table-11-technologies/', views.technology_commercialized_form, name='table_11_form'),

    # New: This is the centralized URL for the multi-sheet Excel export
    path('export-all/', views.export_all_to_excel, name='export_all_to_excel'),
    path('get-curricular-offerings/<int:department_id>/', views.get_curricular_offerings, name='get_curricular_offerings'),
]

