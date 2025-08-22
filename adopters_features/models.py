from django.db import models
from django.conf import settings # Import settings to reference the user model

# ------- Choices (optional cleanup for consistency) -------
SEX_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
]

CATEGORY_CHOICES = [
    ("Student", "Student"),
    ("Farmer", "Farmer"),
    ("Fisherfolk", "Fisherfolk"),
    ("Government Employee", "Government Employee"),
    ("Private Employee", "Private Employee"),
    ("Organization", "Organization"),
    ("Others", "Others"),
]

THEMATIC_CHOICES = [
    ("A", "A - Agri-Fisheries and Food Security"),
    ("B", "B - Biodiversity and Environmental Conservation"),
    ("C", "C - Smart Engineering, ICT and Industrial Competitiveness"),
    ("D", "D - Public Health and Welfare"),
    ("E", "E - Societal Development and Equality"),
]

# ---------------- New Submission Model ----------------
class Submission(models.Model):
    """
    A central model to track each form submission.
    This links the submission details (like who and when) to the specific table data.
    """
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    # The 'submission_id' in your URLs will reference this model's ID.

    def __str__(self):
        return f"Submission by {self.submitter.username} on {self.submitted_at.strftime('%Y-%m-%d')}"

# ---------------- Table 5 - Adopters ----------------
class Table5Adopter(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='table5_data')

    no = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    # 'lead_unit' field has been removed
    related_curricular_offering = models.CharField(max_length=255, blank=True, null=True)

    adopter_name = models.CharField(max_length=255)
    adopter_address = models.TextField(blank=True, null=True)
    adopter_contact = models.CharField(max_length=255, blank=True, null=True)
    adopter_sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    adopter_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)

    projects_involved = models.TextField(blank=True, null=True)
    trainings_attended = models.TextField(blank=True, null=True)
    other_assistance_received = models.TextField(blank=True, null=True)
    date_started = models.DateField(blank=True, null=True)
    technologies_adopted = models.TextField(blank=True, null=True)

    monthly_income_before = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    monthly_income_after = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    income_difference = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    other_significant_changes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    department_unit = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number_email = models.CharField(max_length=255, blank=True, null=True)

    # NEW FIELD ADDED: This will store the supporting documents for Table 5.
    supporting_documents = models.FileField(upload_to='adopter_documents/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-compute income_difference if both values are present
        if self.monthly_income_before is not None and self.monthly_income_after is not None:
            self.income_difference = self.monthly_income_after - self.monthly_income_before
        super().save(*args, **kwargs)

    def __str__(self):
        return self.adopter_name or f"Adopter {self.pk}"


# ---------------- Table 6 - IEC Materials ----------------
class Table6IEC(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='table6_data')
    
    no = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    # 'lead_unit' field has been removed
    related_curricular_offering = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255)
    format = models.CharField(max_length=100, blank=True, null=True)

    male_recipients = models.IntegerField(blank=True, null=True)
    female_recipients = models.IntegerField(blank=True, null=True)
    student_recipients = models.IntegerField(blank=True, null=True)
    farmer_recipients = models.IntegerField(blank=True, null=True)
    fisherfolk_recipients = models.IntegerField(blank=True, null=True)
    ag_technician_recipients = models.IntegerField(blank=True, null=True)
    gov_employee_recipients = models.IntegerField(blank=True, null=True)
    # Renamed field to match the form
    priv_employee_recipients = models.IntegerField(blank=True, null=True)
    # Renamed field to match the form
    other_recipients = models.IntegerField(blank=True, null=True)
    total_recipients = models.IntegerField(blank=True, null=True)

    project_no = models.CharField(max_length=50, blank=True, null=True)
    sdg = models.CharField(max_length=255, blank=True, null=True)
    thematic_area = models.CharField(max_length=255, choices=THEMATIC_CHOICES, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)
    department_unit = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number_email = models.CharField(max_length=255, blank=True, null=True)
    
    # New field to store uploaded files
    supporting_documents = models.FileField(upload_to='iec_documents/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate the total recipients using the corrected field names
        self.total_recipients = (self.male_recipients or 0) + \
                                 (self.female_recipients or 0) + \
                                 (self.student_recipients or 0) + \
                                 (self.farmer_recipients or 0) + \
                                 (self.fisherfolk_recipients or 0) + \
                                 (self.ag_technician_recipients or 0) + \
                                 (self.gov_employee_recipients or 0) + \
                                 (self.priv_employee_recipients or 0) + \
                                 (self.other_recipients or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------------- Table 7a - Budget Utilization (GAA) ----------------
class Table7aBudgetGAA(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='table7a_data')
    
    no = models.IntegerField(blank=True, null=True)
    total_budget_allocated = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    department = models.CharField(max_length=255)
    curricular_offering = models.CharField(max_length=255, blank=True, null=True)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_utilized = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    # New field to store uploaded files
    supporting_documents = models.FileField(upload_to='budget_gaa_documents/', null=True, blank=True)

    def __str__(self):
        return f"GAA - {self.department}"


# ---------------- Table 7b - Budget Utilization (Income) ----------------
class Table7bBudgetIncome(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='table7b_data')
    
    no = models.IntegerField(blank=True, null=True)
    total_budget_allocated = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    department = models.CharField(max_length=255)
    curricular_offering = models.CharField(max_length=255, blank=True, null=True)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_utilized = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # New field to store uploaded files
    supporting_documents = models.FileField(upload_to='budget_income_documents/', null=True, blank=True)

    def __str__(self):
        return f"Income - {self.department}"
