# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.coordinator_auth, name='coordinator_auth'),
    path('logout/', views.coordinator_logout, name='coordinator_logout'),
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/export-all/', views.export_all_submissions, name='export_all_submissions'),
    path('admin-dashboard/view-details/<int:submission_id>/', views.view_submission_details, name='view_submission_details'),
]