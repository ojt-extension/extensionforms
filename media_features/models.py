# models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models



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
    

class Department(models.Model):
    """Represents a department within the institution."""
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'tblDepartment'
        ordering = ['department_name']

class TechnologyStatus(models.Model):
    """A lookup table for the status of a technology."""
    TECHNOLOGY_STATUS_CHOICES = [
        ('DEPLOYED', 'Deployed through various modalities'),
        ('COMMERCIALIZED', 'Commercialized'),
        ('PRE_COMMERCIAL', 'With pre-commercialization activities'),
    ]
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, choices=TECHNOLOGY_STATUS_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_status_name_display()

    class Meta:
        db_table = 'tblTechnologyStatus'
        verbose_name_plural = 'Technology Statuses'

class CurricularOffering(models.Model):
    """Represents a curricular offering or program."""
    curricular_offering_id = models.AutoField(primary_key=True)
    offering_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='curricular_offerings')

    def __str__(self):
        return self.offering_name
    
    class Meta:
        db_table = 'tblCurricularOffering'
        ordering = ['offering_name']


class Technology(models.Model):
    """Represents a technology, including its commercialization details."""
    technology_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='technologies')
    technology_title = models.CharField(max_length=500, verbose_name="Technology Title")
    year_developed = models.IntegerField()
    technology_generator = models.CharField(max_length=255, verbose_name="Technology Generator")
    technology_status = models.ForeignKey(TechnologyStatus, on_delete=models.SET_NULL, null=True, blank=True)
    curricular_offerings = models.ManyToManyField(CurricularOffering, through='TechnologyCurricularOffering')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.technology_title

    class Meta:
        db_table = 'tblTechnology'
        verbose_name_plural = 'Technologies'

# This is the intermediary model for the Many-to-Many relationship
class TechnologyCurricularOffering(models.Model):
    """Junction table for Technology and Curricular Offering."""
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    curricular_offering = models.ForeignKey(CurricularOffering, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tblTechnologyCurricularOffering'
        unique_together = ('technology', 'curricular_offering')


class SupportingDocument(models.Model):
    """
    Model to store multiple documents for a single ExtensionPPAFeatured or Technology record.
    """
    extension_ppa_featured = models.ForeignKey(
        ExtensionPPAFeatured,
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True, # <-- MODIFIED
        blank=True # <-- MODIFIED
    )
    technology = models.ForeignKey( # <-- NEW FOREIGN KEY
        Technology,
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='supporting_documents/')

    def __str__(self):
        if self.extension_ppa_featured:
            return f"Document for {self.extension_ppa_featured.extension_ppa.ppa_name}"
        elif self.technology:
            return f"Document for {self.technology.technology_title}"
        return "Document"
    
    def supporting_documents_list(self):
        return ", ".join([doc.file.url for doc in self.supporting_documents.all()])
    
    def clean(self):
        # Enforce that only one foreign key can be set
        if self.extension_ppa_featured and self.technology:
            raise ValidationError("A supporting document cannot be linked to both a media feature and a technology record.")
        if not self.extension_ppa_featured and not self.technology:
             raise ValidationError("A supporting document must be linked to either a media feature or a technology record.")
