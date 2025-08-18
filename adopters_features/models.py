from django.db import models

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

# ---------------- Table 5 - Adopters ----------------
class Table5Adopter(models.Model):
    no = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    lead_unit = models.CharField(max_length=255, blank=True, null=True)
    related_curricular_offering = models.CharField(max_length=255, blank=True, null=True)

    adopter_name = models.CharField(max_length=255)
    adopter_address = models.TextField(blank=True, null=True)
    adopter_contact = models.CharField(max_length=255, blank=True, null=True)
    adopter_sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    adopter_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)

    projects_involved = models.TextField(blank=True, null=True)
    trainings_attended = models.TextField(blank=True, null=True)          # include dates
    other_assistance_received = models.TextField(blank=True, null=True)   # include dates
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

    def save(self, *args, **kwargs):
        # Auto-compute income_difference if both values are present
        if self.monthly_income_before is not None and self.monthly_income_after is not None:
            self.income_difference = self.monthly_income_after - self.monthly_income_before
        super().save(*args, **kwargs)

    def __str__(self):
        return self.adopter_name or f"Adopter {self.pk}"


# ---------------- Table 6 - IEC Materials ----------------
class Table6IEC(models.Model):
    no = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    lead_unit = models.CharField(max_length=255, blank=True, null=True)
    related_curricular_offering = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255)
    format = models.CharField(max_length=100, blank=True, null=True)  # e.g., video, brochure

    male_recipients = models.IntegerField(blank=True, null=True)
    female_recipients = models.IntegerField(blank=True, null=True)
    student_recipients = models.IntegerField(blank=True, null=True)
    farmer_recipients = models.IntegerField(blank=True, null=True)
    fisherfolk_recipients = models.IntegerField(blank=True, null=True)
    ag_technician_recipients = models.IntegerField(blank=True, null=True)
    gov_employee_recipients = models.IntegerField(blank=True, null=True)
    private_employee_recipients = models.IntegerField(blank=True, null=True)
    others_recipients = models.IntegerField(blank=True, null=True)
    total_recipients = models.IntegerField(blank=True, null=True)

    project_no = models.CharField(max_length=50, blank=True, null=True)   # NA or number
    sdg = models.CharField(max_length=255, blank=True, null=True)         # e.g., "1, 2, 3"
    thematic_area = models.CharField(max_length=255, blank=True, null=True)  # or choices=THEMATIC_CHOICES

    remarks = models.TextField(blank=True, null=True)
    department_unit = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


# ---------------- Table 7a - Budget Utilization (GAA) ----------------
class Table7aBudgetGAA(models.Model):
    total_budget_allocated = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    department = models.CharField(max_length=255)
    curricular_offering = models.CharField(max_length=255, blank=True, null=True)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_utilized = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Disbursed + A/P
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"GAA - {self.department}"


# ---------------- Table 7b - Budget Utilization (Income) ----------------
class Table7bBudgetIncome(models.Model):
    total_budget_allocated = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    department = models.CharField(max_length=255)
    curricular_offering = models.CharField(max_length=255, blank=True, null=True)
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    amount_utilized = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Disbursed + A/P
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Income - {self.department}"
