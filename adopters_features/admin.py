from django.contrib import admin
from .models import Submission, Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

# Register the Submission model to be visible in the admin panel
admin.site.register(Submission)

# --- Admin configuration for Table 5 (Adopters) ---
@admin.register(Table5Adopter)
class Table5AdopterAdmin(admin.ModelAdmin):
    # Fields to display in the list view, as you had them
    list_display = ('no', 'adopter_name', 'department_unit', 'contact_person', 'contact_number_email', 'date_started')
    list_filter = ('department_unit', 'contact_person', 'date_started')
    search_fields = ('adopter_name', 'department_unit')

    # This section makes all fields visible in the detail view
    fieldsets = (
        ('Adopter Information', {
            'fields': (
                'adopter_name', 'adopter_address', 'adopter_contact',
                'adopter_sex', 'adopter_category'
            )
        }),
        ('Project & Assistance Details', {
            'fields': (
                'projects_involved', 'trainings_attended', 'other_assistance_received',
                'date_started', 'technologies_adopted'
            )
        }),
        ('Income and Changes', {
            'fields': (
                'monthly_income_before', 'monthly_income_after', 'income_difference',
                'other_significant_changes', 'remarks'
            )
        }),
        ('Source of Data', {
            'fields': (
                'no', 'code', 'related_curricular_offering', 'department_unit',
                'contact_person', 'contact_number_email', 'submission'
            )
        }),
    )

# --- Admin configuration for Table 6 (IEC Materials) ---
@admin.register(Table6IEC)
class Table6IECAdmin(admin.ModelAdmin):
    # Fields to display in the list view, as you had them
    list_display = ('no', 'title', 'department_unit', 'contact_person', 'contact_number_email')
    list_filter = ('department_unit',)
    search_fields = ('title', 'department_unit')

    # This section makes all fields visible in the detail view
    fieldsets = (
        ('IEC Information', {
            'fields': (
                'title', 'format', 'project_no', 'sdg', 'thematic_area',
                'remarks', 'supporting_documents'
            )
        }),
        ('Recipient Count', {
            'fields': (
                'male_recipients', 'female_recipients', 'student_recipients',
                'farmer_recipients', 'fisherfolk_recipients', 'ag_technician_recipients',
                'gov_employee_recipients', 'priv_employee_recipients', 'other_recipients',
                'total_recipients'
            )
        }),
        ('Source of Data', {
            'fields': (
                'no', 'code', 'related_curricular_offering', 'department_unit',
                'contact_person', 'contact_number_email', 'submission'
            )
        }),
    )

# --- Admin configuration for Table 7a (GAA Budget) ---
@admin.register(Table7aBudgetGAA)
class Table7aBudgetGAAAdmin(admin.ModelAdmin):
    # Fields to display in the list view, as you had them
    list_display = ('department', 'total_budget_allocated', 'allocated_budget', 'amount_utilized', 'remarks')
    list_filter = ('department',)
    search_fields = ('department',)
    
    # This section makes all fields visible in the detail view
    fieldsets = (
        (None, {
            'fields': ('no', 'total_budget_allocated', 'department', 'curricular_offering', 'allocated_budget', 'amount_utilized', 'remarks', 'supporting_documents')
        }),
    )

# --- Admin configuration for Table 7b (Income Budget) ---
@admin.register(Table7bBudgetIncome)
class Table7bBudgetIncomeAdmin(admin.ModelAdmin):
    # Fields to display in the list view, as you had them
    list_display = ('department', 'total_budget_allocated', 'allocated_budget', 'amount_utilized', 'remarks')
    list_filter = ('department',)
    search_fields = ('department',)
    
    # This section makes all fields visible in the detail view
    fieldsets = (
        (None, {
            'fields': ('no', 'total_budget_allocated', 'department', 'curricular_offering', 'allocated_budget', 'amount_utilized', 'remarks', 'supporting_documents')
        }),
    )
