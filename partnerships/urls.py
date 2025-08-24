# automated_report_system/urls.py

from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   #Dashboard
    path('', views.dashboard, name='dashboard'),
    
     # Partnership URLs
    path('partnership-form.html', views.partnership_form, name='partnership_form_html'),
    path('partnership/', views.partnership_form, name='partnership_list'),  # Updated to show form with records
    path('partnership/create/', views.partnership_form, name='partnership_form'),



    # Internal Project URLs
    path('internal-form.html', views.internal_project_form, name='internal_form_html'),
    path('internal-projects/', views.internal_project_form, name='internal_project_list'),  # Updated to show form with records
    path('internal-projects/create/', views.internal_project_form, name='internal_project_form'),



    # External Project URLs
    path('external-form.html', views.external_project_form, name='external_form_html'),
    path('external-projects/', views.external_project_form, name='external_project_list'),  # Updated to show form with records
    path('external-projects/create/', views.external_project_form, name='external_project_form'),



    # Advisory Services URLs
    path('advisory-form.html', views.advisory_services_form, name='advisory_form_html'),
    path('advisory-services/', views.advisory_services_form, name='advisory_services_list'),  # Updated to show form with records
    path('advisory-services/create/', views.advisory_services_form, name='advisory_services_form'),



    # Combined Records List (lists.html)
    path('lists.html', views.partnership_list, name='records_list_html'),

    # Utility URLs
    path('partnership/<int:partnership_id>/select-form/', views.select_form_type, name='select_form_type'),

    # API URLs
    path('api/partnership/<int:partnership_id>/', views.get_partnership_data, name='get_partnership_data'),
    path('api/partnerships/', views.get_partnerships_by_nature, name='get_partnerships_by_nature'),
    
    # Export URLs
    path('export/forms/', views.export_forms_to_excel, name='export_forms'),
    path('export/partnerships/', views.export_partnerships, name='export_partnerships'),
    path('export/internal-projects/', views.export_internal_projects, name='export_internal_projects'),
    path('export/external-projects/', views.export_external_projects, name='export_external_projects'),
    path('export/advisory-services/', views.export_advisory_services, name='export_advisory_services'),
    path('export/all/', views.export_all_data, name='export_all_data'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)