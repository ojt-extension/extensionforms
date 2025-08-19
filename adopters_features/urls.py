from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Table 5
    path('table5/', views.table5_view, name='table5'),
    path('table5/edit/<int:pk>/', views.table5_edit, name='table5_edit'),
    path('table5/delete/<int:pk>/', views.table5_delete, name='table5_delete'),
    path('export/table5/', views.export_table5_excel, name='export_table5'),
    # Bagong URL para sa view details ng Table 5
    path('admin/table5/<int:submission_id>/', views.view_submission_details, name='table5_details'),

    # Table 6
    path('table6/', views.table6_view, name='table6'),
    path('table6/edit/<int:pk>/', views.table6_edit, name='table6_edit'),
    path('table6/delete/<int:pk>/', views.table6_delete, name='table6_delete'),
    path('export/table6/', views.export_table6_excel, name='export_table6'),
    # Bagong URL para sa view details ng Table 6
    path('admin/table6/<int:submission_id>/', views.view_submission_details, name='table6_details'),

    # Table 7a
    path('table7a/', views.table7a_view, name='table7a'),
    path('table7a/edit/<int:pk>/', views.table7a_edit, name='table7a_edit'),
    path('table7a/delete/<int:pk>/', views.table7a_delete, name='table7a_delete'),
    path('export/table7a/', views.export_table7a_excel, name='export_table7a'),
    # Bagong URL para sa view details ng Table 7a
    path('admin/table7a/<int:submission_id>/', views.view_submission_details, name='table7a_details'),

    # Table 7b
    path('table7b/', views.table7b_view, name='table7b'),
    path('table7b/edit/<int:pk>/', views.table7b_edit, name='table7b_edit'),
    path('table7b/delete/<int:pk>/', views.table7b_delete, name='table7b_delete'),
    path('export/table7b/', views.export_table7b_excel, name='export_table7b'),
    # Bagong URL para sa view details ng Table 7b
    path('admin/table7b/<int:submission_id>/', views.view_submission_details, name='table7b_details'),

    # Export All
    path('export/all/', views.export_all_excel, name='export_all'),
]
