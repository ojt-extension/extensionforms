from django.urls import path
from . import views



urlpatterns = [
    # New: This is the URL for the main dashboard listing all forms
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('table-3-trainings/', views.training_form, name='table_3_form'),
    path('table-8-faculty-involvement/', views.faculty_involvement_form, name='table_8_form'),
    path('table-9-student-involvement/', views.student_involvement_form, name='table_9_form'),
    path('table-10-media-features/', views.media_feature_form, name='table_10_form'),
    path('table-11-technologies/', views.technology_commercialized_form, name='table_11_form'),
    path('table-12-ordinance/', views.ordinance_form, name='table_12_form'),
    path('table-13-impact-assessment/', views.impact_assessment_form, name='table_13_form'),
    path('table-14-awards/', views.awards_form, name='table_14_form'),
    path('table-15-other-activities/', views.other_activities_form, name='table_15_form'),

    # New: This is the centralized URL for the multi-sheet Excel export
    path('export-all/', views.export_all_to_excel, name='export_all_to_excel'),
    path('get-curricular-offerings/<int:department_id>/', views.get_curricular_offerings, name='get_curricular_offerings'),
]

