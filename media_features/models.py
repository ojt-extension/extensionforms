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
    TECHNOLOGY_STATUS_CHOICES = (
        ('DEPLOYED', 'Deployed through various modalities'),
        ('COMMERCIALIZED', 'Commercialized'),
        ('PRE_COMMERCIAL', 'With pre-commercialization activities'),
    )
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

# Choices for Academic Ranks
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

class Ordinance(models.Model):
    """Model for Ordinances"""
    ordinance_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ordinances')
    curricular_offering = models.ForeignKey(CurricularOffering, on_delete=models.CASCADE, related_name='ordinances', null=True, blank=True)
    extension_ppa = models.ForeignKey(ExtensionPPA, on_delete=models.CASCADE, related_name='ordinances', null=True, blank=True)
    ordinance_title = models.CharField(max_length=500)
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DRAFT')
    date_approved = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.ordinance_title
    
    class Meta:
        db_table = 'tblOrdinance'
        ordering = ['-date_approved']


class ImpactAssessment(models.Model):
    """Model for Impact Assessments"""
    assessment_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='impact_assessments')
    curricular_offering = models.ForeignKey(CurricularOffering, on_delete=models.CASCADE, related_name='impact_assessments')
    extension_ppa_ia = models.ForeignKey(ExtensionPPA, on_delete=models.CASCADE, related_name='impact_assessments')
    proponent_ias = models.CharField(max_length=255, verbose_name="Proponent/IAs")
    date_conducted = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Impact Assessment - {self.department.department_name}"
    
    class Meta:
        db_table = 'tblImpactAssessment'
        ordering = ['-date_conducted']


class Awards(models.Model):
    """Model for Awards"""
    award_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='awards')
    person_received_award = models.CharField(max_length=255)
    award_title = models.CharField(max_length=500)
    award_donor = models.CharField(max_length=255)
    LEVEL_CHOICES = [   
        ('LOCAL', 'Local'),
        ('REGIONAL', 'Regional'),
        ('NATIONAL', 'National'),
        ('INTERNATIONAL', 'International'),
    ]
    level_of_award = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    date_received = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.award_title} - {self.person_received_award}"
    
    class Meta:
        db_table = 'tblAwards'
        ordering = ['-date_received']


class OtherActivities(models.Model):
    """Model for Other Activities"""
    activity_id = models.AutoField(primary_key=True)
    date_conducted = models.DateField()
    activity_title = models.CharField(max_length=500)
    CATEGORY_CHOICES = [
        ('MEETING', 'Meeting'),
        ('WORKSHOP', 'Workshop'),
        ('PLANNING', 'Planning'),
        ('CAPACITY_BUILDING', 'Capacity Building for Extensionists'),
        ('COMMUNITY_OUTREACH_ACTIVITY', 'Community Outreach Activity'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    participants = models.CharField(max_length=255, verbose_name="Number/Type of Partipants")
    purpose = models.TextField()
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_of_funds = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.activity_title
    
    class Meta:
        db_table = 'tblOtherActivities'
        ordering = ['-date_conducted']

class CollaboratingAgency(models.Model):
    """Represents collaborating agencies for training programs"""
    agency_id = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.agency_name
    
    class Meta:
        db_table = 'tblCollaboratingAgency'
        verbose_name_plural = 'Collaborating Agencies'
        ordering = ['agency_name']

class TrainingCategory(models.Model):
    """Lookup table for training categories"""
    CATEGORY_CHOICES = [
        ('TVL', 'Technical, Vocational, Livelihood'),
        ('AE', 'Agricultural and Environmental Trainings'),
        ('CE', 'Continuing Education for Professionals'),
        ('BE', 'Basic Education'),
        ('GAD', 'Gender and Development'),
        ('O', 'Others'),
    ]
    
    category_id = models.AutoField(primary_key=True)
    category_code = models.CharField(max_length=10, choices=CATEGORY_CHOICES, unique=True)
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.category_code} - {self.category_name}"
    
    class Meta:
        db_table = 'tblTrainingCategory'
        verbose_name_plural = 'Training Categories'

class SustainableDevelopmentGoal(models.Model):
    """Lookup table for UN Sustainable Development Goals"""
    sdg_id = models.AutoField(primary_key=True)
    sdg_number = models.IntegerField(unique=True)
    sdg_title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"SDG {self.sdg_number}: {self.sdg_title}"
    
    class Meta:
        db_table = 'tblSustainableDevelopmentGoal'
        ordering = ['sdg_number']

class ThematicArea(models.Model):
    """Lookup table for thematic areas"""
    THEMATIC_CHOICES = [
        ('A', 'Agri-Fisheries and Food Security'),
        ('B', 'Biodiversity and Environmental Conservation'),
        ('C', 'Smart Engineering, ICT and Industrial Competitiveness'),
        ('D', 'Public Health and Welfare'),
        ('E', 'Societal Development and Equality'),
    ]
    
    thematic_area_id = models.AutoField(primary_key=True)
    thematic_code = models.CharField(max_length=10, choices=THEMATIC_CHOICES, unique=True)
    thematic_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.thematic_code} - {self.thematic_name}"
    
    class Meta:
        db_table = 'tblThematicArea'
        verbose_name_plural = 'Thematic Areas'

class Training(models.Model):
    """Main training record model"""
    training_id = models.AutoField(primary_key=True)
    training_no = models.CharField(max_length=50, unique=True, verbose_name="Training No.")
    extension_code = models.CharField(max_length=50, verbose_name="Code (c/o Extension Services)")
    
    # Lead Unit Information
    lead_department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='led_trainings',
        verbose_name="Lead Department"
    )
    contact_person = models.CharField(max_length=255, verbose_name="Contact Person")
    contact_number_email = models.CharField(max_length=255, verbose_name="Number/Email")
    
    # Curricular Offering - Many-to-many relationship
    curricular_offerings = models.ManyToManyField(
        CurricularOffering,
        blank=True,
        verbose_name="Curricular Offerings"
    )
    
    # Collaborating Agency Information
    collaborating_agencies = models.ManyToManyField(
        CollaboratingAgency,
        blank=True,
        verbose_name="Collaborating Agencies"
    )
    training_coordinator = models.CharField(max_length=255, verbose_name="Training Coordinator")
    
    # Project and Category Information
    project_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Project No.")
    category = models.ForeignKey(
        TrainingCategory,
        on_delete=models.CASCADE,
        verbose_name="Category"
    )
    
    # Training Details
    title = models.CharField(max_length=500, verbose_name="Title of Training")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    venue = models.CharField(max_length=500, verbose_name="Venue")
    
    # Participants by Sex
    male_participants = models.IntegerField(default=0, verbose_name="Male Participants")
    female_participants = models.IntegerField(default=0, verbose_name="Female Participants")
    prefer_not_to_say_participants = models.IntegerField(default=0, verbose_name="Prefer Not To Say")
    
    # Participants by Category
    student_participants = models.IntegerField(default=0, verbose_name="Student Participants")
    farmer_participants = models.IntegerField(default=0, verbose_name="Farmer Participants")
    fisherfolk_participants = models.IntegerField(default=0, verbose_name="Fisherfolk Participants")
    ag_technician_participants = models.IntegerField(default=0, verbose_name="Ag Technician Participants")
    government_employee_participants = models.IntegerField(default=0, verbose_name="Government Employee Participants")
    private_employee_participants = models.IntegerField(default=0, verbose_name="Private Employee Participants")
    four_ps_participants = models.IntegerField(default=0, verbose_name="4P's Participants")
    other_participants = models.IntegerField(default=0, verbose_name="Other Participants")
    
    # TVL Training Specific Fields
    solo_parent_participants = models.IntegerField(default=0, verbose_name="Solo Parent Participants (TVL only)")
    four_ps_members = models.IntegerField(default=0, verbose_name="4P's Members (TVL only)")
    participants_with_disabilities = models.IntegerField(default=0, verbose_name="Participants with Disabilities (TVL only)")
    
    # Training Duration and Weight
    DURATION_CHOICES = [
        ('5_plus', '5 or more days (x2.00)'),
        ('3_to_4', '3 to 4 days (x1.5)'),
        ('2_days', '2 days (x1.25)'),
        ('1_day', '1 day (8 hours) (x1.00)'),
        ('less_than_1', 'Less than 1 day or 8 hours (x0.5)'),
    ]
    
    training_duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        verbose_name="Number of Days Trained"
    )
    
    # Survey and Rating Information
    total_trainees_surveyed = models.IntegerField(verbose_name="Total No. Of Trainees Surveyed")
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    relevance_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="Client's Rating on Training Relevance"
    )
    quality_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="Client's Rating on Training Quality"
    )
    timeliness_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name="Client's Rating on Training Timeliness"
    )
    
    # Request Information
    total_clients_requesting = models.IntegerField(verbose_name="Total No. of Clients Requesting Trainings")
    requests_responded_3_days = models.IntegerField(verbose_name="Requests Responded in Next 3 Days")
    
    # Financial Information
    amount_charged_cvsu = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Amount Charged to CvSU"
    )
    amount_charged_partner = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Amount Charged to Partner Agency"
    )
    partner_agency_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Name of Partner Agency"
    )
    
    # Classification
    sustainable_development_goal = models.ForeignKey(
        SustainableDevelopmentGoal,
        on_delete=models.CASCADE,
        verbose_name="Sustainable Development Goal"
    )
    thematic_area = models.ForeignKey(
        ThematicArea,
        on_delete=models.CASCADE,
        verbose_name="Thematic Area"
    )
    
    # Additional Information
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_participants_by_sex(self):
        """Calculate total participants by sex"""
        return self.male_participants + self.female_participants + self.prefer_not_to_say_participants
    
    @property
    def total_participants_by_category(self):
        """Calculate total participants by category"""
        return (self.student_participants + self.farmer_participants + 
                self.fisherfolk_participants + self.ag_technician_participants +
                self.government_employee_participants + self.private_employee_participants +
                self.four_ps_participants + self.other_participants)
    
    @property
    def training_weight_multiplier(self):
        """Get the training weight multiplier based on duration"""
        weight_map = {
            '5_plus': 2.00,
            '3_to_4': 1.5,
            '2_days': 1.25,
            '1_day': 1.00,
            'less_than_1': 0.5,
        }
        return weight_map.get(self.training_duration, 1.0)
    
    @property
    def weighted_training_days(self):
        """Calculate weighted training days"""
        return self.total_participants_by_sex * self.training_weight_multiplier
    
    @property
    def inclusive_dates(self):
        """Get formatted inclusive dates"""
        if self.start_date == self.end_date:
            return self.start_date.strftime("%B %d, %Y")
        return f"{self.start_date.strftime('%B %d, %Y')} - {self.end_date.strftime('%B %d, %Y')}"
    
    def clean(self):
        """Model validation"""
        super().clean()
        
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")
        
        # Validate that TVL-specific fields are only used for TVL category
        if self.category and self.category.category_code != 'TVL':
            if (self.solo_parent_participants > 0 or 
                self.four_ps_members > 0 or 
                self.participants_with_disabilities > 0):
                raise ValidationError(
                    "Solo parent, 4P's members, and participants with disabilities "
                    "fields are only for TVL trainings."
                )
    
    def __str__(self):
        return f"{self.training_no} - {self.title}"
    
    class Meta:
        db_table = 'tblTraining'
        ordering = ['-start_date', 'training_no']
        verbose_name = "Training"
        verbose_name_plural = "Trainings"

class SupportingDocument(models.Model):
    """
    Model to store multiple documents. 
    """
    training = models.ForeignKey(
        'Training',
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )

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
    ordinance = models.ForeignKey(
        'Ordinance',
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    impact_assessment = models.ForeignKey(
        'ImpactAssessment', 
        on_delete=models.CASCADE,
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    award = models.ForeignKey(
        'Awards',
        on_delete=models.CASCADE, 
        related_name='supporting_documents',
        null=True,
        blank=True
    )
    other_activity = models.ForeignKey(
        'OtherActivities',
        on_delete=models.CASCADE,
        related_name='supporting_documents', 
        null=True,
        blank=True
    )   
    
    file = models.FileField(upload_to='supporting_documents/')
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        if self.training:
            return f"Document for {self.training.training_no} - {self.training.title}"
        elif self.extension_ppa_featured:
            return f"Document for {self.extension_ppa_featured.extension_ppa.ppa_name}"
        elif self.technology:
            return f"Document for {self.technology.technology_title}"
        elif self.student_involvement:
            return f"Document for {self.student_involvement.department.department_name} - {self.student_involvement.curricular_offering.offering_name}"
        elif self.faculty_involvement: 
            return f"Document for {self.faculty_involvement.faculty_staff_name}"
        elif self.ordinance:
            return f"Document for {self.ordinance.ordinance_title}"
        elif self.impact_assessment:
            return f"Document for Impact Assessment - {self.impact_assessment.department.department_name}"
        elif self.award:
            return f"Document for {self.award.award_title} - {self.award.person_received_award}"
        elif self.other_activity:
            return f"Document for {self.other_activity.activity_title}"
        return "Document"
    
    def clean(self):
        # Update validation to include the new field
        fields_set = sum([
            bool(self.training),
            bool(self.extension_ppa_featured),
            bool(self.technology),
            bool(self.student_involvement),
            bool(self.faculty_involvement),
            bool(self.ordinance),
            bool(self.impact_assessment),
            bool(self.award),
            bool(self.other_activity)
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

