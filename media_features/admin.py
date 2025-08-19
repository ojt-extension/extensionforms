#media_features\admin.py
from django.contrib import admin
from .models import ExtensionPPA, MediaOutlet, ExtensionPPAFeatured, Department, TechnologyStatus, CurricularOffering, Technology
from .models import (
    Training,
    CollaboratingAgency,
    Project,
    Category,
    ThematicArea,
    LeadUnit,
    Department,
    ContactPerson,
    CurricularOffering,
    TrainingCollaboratingAgency,
)


@admin.register(ExtensionPPA)
class ExtensionPPAAdmin(admin.ModelAdmin):
    list_display = ['ppa_name', 'extension_ppa_id']
    search_fields = ['ppa_name']
    ordering = ['ppa_name']

@admin.register(MediaOutlet)
class MediaOutletAdmin(admin.ModelAdmin):
    list_display = ['media_outlet_name', 'media_type', 'media_outlet_id']
    list_filter = ['media_type']
    search_fields = ['media_outlet_name']
    ordering = ['media_outlet_name']

@admin.register(ExtensionPPAFeatured)
class ExtensionPPAFeaturedAdmin(admin.ModelAdmin):
    list_display = ['extension_ppa', 'media_outlet', 'date_featured']
    list_filter = ['date_featured', 'media_outlet__media_type']
    search_fields = ['extension_ppa__ppa_name', 'media_outlet__media_outlet_name']
    date_hierarchy = 'date_featured'
    ordering = ['-date_featured']
    
    fieldsets = (
        ('PPA Information', {
            'fields': ('extension_ppa',)
        }),
        ('Media Information', {
            'fields': ('media_outlet', 'date_featured')
        }),
        ('Additional Details', {
            'fields': ('remarks',)
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name']
    search_fields = ['department_name']

@admin.register(TechnologyStatus)
class TechnologyStatusAdmin(admin.ModelAdmin):
    list_display = ['status_name']

@admin.register(CurricularOffering)
class CurricularOfferingAdmin(admin.ModelAdmin):
    list_display = ['offering_name', 'department']
    list_filter = ['department']
    search_fields = ['offering_name']

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['technology_title', 'department', 'year_developed', 'technology_status']
    list_filter = ['department', 'year_developed', 'technology_status']
    search_fields = ['technology_title', 'technology_generator']

admin.site.register(Training)
admin.site.register(CollaboratingAgency)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ThematicArea)
admin.site.register(ContactPerson)
admin.site.register(TrainingCollaboratingAgency)
