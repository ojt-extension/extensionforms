# models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from accounts.models import CustomUser 
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

class StudentExtensionInvolvement(models.Model):
    """Represents student involvement in extension activities by department and curricular offering."""
    student_involvement_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='student_involvements')
    curricular_offering = models.ForeignKey(CurricularOffering, on_delete=models.CASCADE, related_name='student_involvements')
    total_students_for_period = models.IntegerField(verbose_name="Total Number of Students for the period (a)")
    students_involved_in_extension = models.IntegerField(verbose_name="Number of Students involved in extension activities (b)")
    percentage_students_involved = models.FloatField(verbose_name="Percentage of Students involved (%)", editable=False)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Automatically calculate the percentage
        if self.total_students_for_period and self.total_students_for_period > 0:
            self.percentage_students_involved = (self.students_involved_in_extension / self.total_students_for_period) * 100
        else:
            self.percentage_students_involved = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.department.department_name} - {self.curricular_offering.offering_name}"

    class Meta:
        db_table = 'tblStudentExtensionInvolvement'
        verbose_name = 'Student Extension Involvement'
        verbose_name_plural = 'Student Extension Involvements'
        ordering = ['-created_at']

ACADEMIC_RANKS = (
    ('Instructor I', 'Instructor I'),
    ('Instructor II', 'Instructor II'),
    ('Instructor III', 'Instructor III'),
    ('Assistant Professor', 'Assistant Professor'),
    ('Assistant Professor I', 'Assistant Professor I'),
    ('Assistant Professor II', 'Assistant Professor II'),
    ('Assistant Professor III', 'Assistant Professor III'),
    ('Assistant Professor IV', 'Assistant Professor IV'),
    ('Associate Professor', 'Associate Professor'),
    ('Associate Professor I', 'Associate Professor I'),
    ('Associate Professor II', 'Associate Professor II'),
    ('Associate Professor III', 'Associate Professor III'),
    ('Associate Professor V', 'Associate Professor V'),
    ('Professor', 'Professor'),
    ('Professor VI', 'Professor VI'),
    ('University Professor', 'University Professor'),
)

# Choices for Employment Status
EMPLOYMENT_STATUSES = (
    ('Permanent', 'Permanent'),
    ('COS', 'COS'),
    ('JO', 'JO'),
)

class FacultyInvolvement(models.Model):
    """
    Model for Table 8: Faculty Involvement in ESCE.
    """
    submitter = models.ForeignKey(
        CustomUser, # Use your custom user model
        on_delete=models.SET_NULL,
        null=True,
        related_name='faculty_involvement_submissions',
        verbose_name="Submitter"
    )
    faculty_staff_name = models.CharField(max_length=255, verbose_name="Name of Faculty/Staff (Last, First MI.)")
    academic_rank_position = models.CharField(
        max_length=255,
        choices=ACADEMIC_RANKS,
        verbose_name="Academic Rank (Faculty)/ Position (Staff)"
    )
    employment_status = models.CharField(
        max_length=255,
        choices=EMPLOYMENT_STATUSES,
        verbose_name="Employment Status"
    )
    avg_hours_per_week = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Average number of hours engaged in Extension activities (per week)"
    )
    total_hours_per_quarter = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Total Number of hours engaged in Extension activities for the period/quarter"
    )
    remarks = models.TextField(blank=True, verbose_name="Remarks")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tblFacultyInvolvement'
        verbose_name = "Faculty Involvement"
        verbose_name_plural = "Faculty Involvement"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"T8: {self.faculty_staff_name}"

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
    student_involvement = models.ForeignKey(
        StudentExtensionInvolvement,
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    faculty_involvement = models.ForeignKey(
        'FacultyInvolvement',
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='supporting_documents/')
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        if self.extension_ppa_featured:
            return f"Document for {self.extension_ppa_featured.extension_ppa.ppa_name}"
        elif self.technology:
            return f"Document for {self.technology.technology_title}"
        elif self.student_involvement:
            return f"Document for {self.student_involvement.department.department_name} - {self.student_involvement.curricular_offering.offering_name}"
        elif self.faculty_involvement: # <-- NEW condition
            return f"Document for {self.faculty_involvement.faculty_staff_name}"
        return "Document"
    
    def clean(self):
        # Update validation to include the new field
        fields_set = sum([
            bool(self.extension_ppa_featured),
            bool(self.technology),
            bool(self.student_involvement),
            bool(self.faculty_involvement)
        ])
        
        if fields_set > 1:
            raise ValidationError("A supporting document can only be linked to one type of record.")
        if fields_set == 0:
            raise ValidationError("A supporting document must be linked to a record.")

class FormSubmission(models.Model):
    """
    Model to store submitted forms from OJT Coordinators.
    """
    # Link the submission to the user who submitted it
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')

    # Store a reference to which form was submitted (e.g., 'Table 10', 'Table 11')
    form_name = models.CharField(max_length=100)

    # Store the actual form data. A JSONField is flexible for various forms.
    form_data = models.JSONField()

    # The date and time the form was submitted
    submitted_at = models.DateTimeField(default=timezone.now)

    form_instance_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.form_name} submitted by {self.submitter.get_full_name()} on {self.submitted_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-submitted_at']



