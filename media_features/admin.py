from django.contrib import admin
from .models import ExtensionPPA, MediaOutlet, ExtensionPPAFeatured

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