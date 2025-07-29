from django.db import models
from django.utils import timezone

class MediaOutlet(models.Model):
    """Represents different media outlets where PPAs can be featured"""
    media_outlet_id = models.AutoField(primary_key=True)
    media_outlet_name = models.CharField(max_length=255)
    media_type = models.CharField(
        max_length=50,
        choices=[
            ('PRINT', 'Print Media'),
            ('RADIO', 'Radio'),
            ('TV', 'Television'),
            ('ONLINE', 'Online/Website'),
            ('SOCIAL', 'Social Media'),
        ]
    )
    
    def __str__(self):
        return f"{self.media_outlet_name} ({self.get_media_type_display()})"
    
    class Meta:
        db_table = 'tblMediaOutlet'
        ordering = ['media_outlet_name']

class ExtensionPPA(models.Model):
    """Represents Extension Programs, Projects, or Activities"""
    extension_ppa_id = models.AutoField(primary_key=True)
    ppa_name = models.CharField(max_length=500, verbose_name="PPA Title")
    
    def __str__(self):
        return self.ppa_name
    
    class Meta:
        db_table = 'tblExtensionPPA'
        verbose_name = "Extension PPA"
        verbose_name_plural = "Extension PPAs"

class ExtensionPPAFeatured(models.Model):
    """Records when and where PPAs were featured in media"""
    extension_ppa_featured_id = models.AutoField(primary_key=True)
    extension_ppa = models.ForeignKey(
        ExtensionPPA, 
        on_delete=models.CASCADE,
        related_name='features'
    )
    media_outlet = models.ForeignKey(
        MediaOutlet,
        on_delete=models.CASCADE,
        related_name='featured_ppas'
    )
    date_featured = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.extension_ppa.ppa_name} - {self.media_outlet.media_outlet_name} ({self.date_featured})"
    
    class Meta:
        db_table = 'tblExtensionPPAFeatured'
        ordering = ['-date_featured']
        verbose_name = "PPA Media Feature"
        verbose_name_plural = "PPA Media Features"