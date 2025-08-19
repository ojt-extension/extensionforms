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


class LeadUnit(models.Model):
    """Represents a lead unit, such as a college or campus."""
    lead_unit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tblLeadUnit'
        verbose_name = 'Lead Unit'
        verbose_name_plural = 'Lead Units'
    
class Department(models.Model):
    """Represents a department within the institution, linked to a Lead Unit."""
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    lead_unit = models.ForeignKey(
        'LeadUnit',
        on_delete=models.SET_NULL,
        null=True,  # This allows the database to store null for existing records
        blank=True, # This allows the field to be optional in forms
        verbose_name="Lead Unit"
    )


    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'tblDepartment'
        ordering = ['department_name']
        verbose_name = 'Lead Unit Department/Unit'
        verbose_name_plural = 'Lead Unit Departments/Units'

class ContactPerson(models.Model):
    """Represents a contact person for a department or unit."""
    contact_person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    number_email = models.CharField(max_length=255, verbose_name="Number/Email")
    role = models.CharField(max_length=100, help_text="e.g., Training Coordinator")
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='contact_persons'
    )
    
    def __str__(self):
        return f"{self.name} ({self.role})"
        
    class Meta:
        db_table = 'tblContactPerson'
        verbose_name_plural = 'Contact Persons'

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
    training = models.ForeignKey(
        'Training', 
        on_delete=models.CASCADE, 
        related_name='supporting_documents',
        null=True, blank=True
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
    file = models.FileField(upload_to='supporting_documents/')
    submitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        if self.training:
            return f"Document for Training: {self.training.TitleOfTraining}"
        elif self.extension_ppa_featured:
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


class Category(models.Model):
    """A lookup table for training categories."""
    CATEGORY_CHOICES = [
        ('TVL', 'TVL - technical, vocational, livelihood'),
        ('AE', 'AE - agricultural and environmental trainings'),
        ('CE', 'CE - continuing education for professionals'),
        ('BE', 'BE - basic education'),
        ('GAD', 'GAD - Gender and Development'),
        ('O', 'O - others'),
    ]
    category_code = models.CharField(max_length=50, choices=CATEGORY_CHOICES, primary_key=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_category_code_display()

    class Meta:
        db_table = 'tblTrainingCategory'
        verbose_name_plural = 'Categories'

class ThematicArea(models.Model):
    """A lookup table for thematic areas."""
    AREA_CHOICES = [
        ('A', 'A- Agri-Fisheries and Food Security'),
        ('B', 'B-Biodiversity and Environmental Conservation'),
        ('C', 'C-Smart Engineering, ICT and Industrial Competitiveness'),
        ('D', 'D-Public Health and Welfare'),
        ('E', 'E-Societal Development and Equality'),
    ]
    area_code = models.CharField(max_length=50, choices=AREA_CHOICES, primary_key=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_area_code_display()

    class Meta:
        db_table = 'tblThematicArea'
        verbose_name_plural = 'Thematic Areas'

class Project(models.Model):
    """Represents internally or externally funded projects."""
    project_no = models.CharField(max_length=100, primary_key=True)
    project_title = models.CharField(max_length=500, verbose_name="Project Title")
    
    def __str__(self):
        return f"{self.project_no}: {self.project_title}"
    
    class Meta:
        db_table = 'tblProject'

class Training(models.Model):
    """The main model for trainings (Table 3)."""
    TRAINING_DAYS_CHOICES = [
        ('5+', '5 or more days (x 2.00)'),
        ('3-4', '3 to 4 days (x 1.5)'),
        ('2', '2 days (x 1.25)'),
        ('1', '1 day (8 hours) (x 1.00)'),
        ('less_1', 'Less than 1 day or 8 hours (x 0.5)'),
    ]
    
    training_no = models.CharField(max_length=100, null=True, blank=True)
    Code = models.CharField(max_length=100, verbose_name="Code (c/o Extension Services)", blank=True, null=True)
    TitleOfTraining = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Project No.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    InclusiveDates = models.CharField(max_length=255, verbose_name="Inclusive Dates")
    Venue = models.CharField(max_length=255)
    
    # Lead Unit info
    lead_unit = models.ForeignKey('LeadUnit', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lead Unit Department/Unit")
    contact_person = models.CharField(max_length=255, verbose_name="Contact Person", blank=True, null=True)
    contact_number_email = models.CharField(max_length=255, verbose_name="Number/Email", blank=True, null=True)
    
    related_curricular_offering = models.CharField(max_length=500, verbose_name="Related Curricular Offering (e.g. BS Agriculture)")
    
    total_male = models.IntegerField(default=0, verbose_name="Male")
    total_female = models.IntegerField(default=0, verbose_name="Female")
    total_prefer_no_to_say = models.IntegerField(default=0, verbose_name="Prefer not to say")
    Total_participants_by_sex = models.IntegerField(default=0, editable=False)

    # Participant counts by category
    student_count = models.IntegerField(default=0, verbose_name="Student")
    farmer_count = models.IntegerField(default=0, verbose_name="Farmer")
    fisherfolk_count = models.IntegerField(default=0, verbose_name="Fisherfolk")
    ag_technician_count = models.IntegerField(default=0, verbose_name="Ag Technician")
    government_employee_count = models.IntegerField(default=0, verbose_name="Government Employee")
    private_employee_count = models.IntegerField(default=0, verbose_name="Private Employee")
    fourps_count = models.IntegerField(default=0, verbose_name="4Ps")
    others_count = models.IntegerField(default=0, verbose_name="Others")
    Total_participants_by_category = models.IntegerField(default=0, editable=False)

    # TVL Specific Fields
    solo_parent_count = models.IntegerField(default=0, verbose_name="No. of participants who are solo parent", blank=True, null=True)
    fourps_members_count = models.IntegerField(default=0, verbose_name="No. of participants who are 4Ps members", blank=True, null=True)
    pwd_count = models.IntegerField(default=0, verbose_name="No. of participants with disabilities", blank=True, null=True)
    type_of_disability = models.CharField(max_length=255, verbose_name="Type of disability", blank=True, null=True)

    TotalNoOfPersonsTrained = models.IntegerField(default=0, editable=False)
    Number_of_days_trained = models.CharField(max_length=20, choices=TRAINING_DAYS_CHOICES, verbose_name="Number of days trained")
    Number_of_days_trained_weight = models.FloatField(verbose_name="Number of days trained per weight of training", editable=False)
    TotalNoOfTraineesSurveyed = models.IntegerField(default=0)
    ClientRatingRelevance = models.IntegerField(verbose_name="Client's rating on the training (relevance)", blank=True, null=True)
    ClientRatingQuality = models.IntegerField(verbose_name="Client's rating on the training (quality)", blank=True, null=True)
    ClientRatingTimeliness = models.IntegerField(verbose_name="Client's rating on the training (timeliness)", blank=True, null=True)
    TotalNumberofClientsRequestingTrainings = models.IntegerField(default=0)
    TotalNumberofRequestsResponded = models.IntegerField(default=0)
    
    sustainable_development_goal = models.CharField(max_length=255, verbose_name="Sustainable Development Goal", blank=True, null=True)
    thematic_area = models.ForeignKey(ThematicArea, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate Total Participants by Sex
        self.Total_participants_by_sex = (
            self.total_male + self.total_female + self.total_prefer_no_to_say
        )

        # Calculate Total Participants by Category
        self.Total_participants_by_category = (
            self.student_count + self.farmer_count + self.fisherfolk_count +
            self.ag_technician_count + self.government_employee_count +
            self.private_employee_count + self.fourps_count + self.others_count
        )

        # Calculate Total No. of Persons Trained (sum of all participant counts)
        self.TotalNoOfPersonsTrained = (
            self.Total_participants_by_sex + self.Total_participants_by_category
        )

        # Assign weight based on Number_of_days_trained
        weights = {
            '5+': 2.00,
            '3-4': 1.5,
            '2': 1.25,
            '1': 1.00,
            'less_1': 0.5
        }
        self.Number_of_days_trained_weight = weights.get(self.Number_of_days_trained, 0.0)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.TitleOfTraining

    class Meta:
        db_table = 'tblTraining'
        verbose_name_plural = 'Trainings'

    supporting_document = models.FileField(
        upload_to='training_documents/',
        verbose_name="Supporting Document",
        blank=True,
        null=True
    )

class CollaboratingAgency(models.Model):
    """Represents a collaborating agency for a training."""
    agency_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Name of Partner Agency")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tblCollaboratingAgency'
        verbose_name_plural = 'Collaborating Agencies'

class TrainingCollaboratingAgency(models.Model):
    """Junction table for Training and Collaborating Agency."""
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    agency = models.ForeignKey(CollaboratingAgency, on_delete=models.CASCADE)
    amount_charged_to_cvsu = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount charged to CvSU", blank=True, null=True)
    amount_charged_to_partner = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount charged to partner agency", blank=True, null=True)

    class Meta:
        db_table = 'tblTrainingCollaboratingAgency'
        unique_together = ('training', 'agency')