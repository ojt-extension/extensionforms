from django import forms
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

class Table5Form(forms.ModelForm):
    # This field is defined here, but it also needs to be added to the Meta.fields tuple.
    supporting_documents = forms.FileField(required=False)
    
    class Meta:
        model = Table5Adopter
        fields = (
            'no', 'code', 'related_curricular_offering', 'adopter_name', 
            'adopter_address', 'adopter_contact', 'adopter_sex', 
            'adopter_category', 'projects_involved', 'trainings_attended',
            'other_assistance_received', 'date_started', 'technologies_adopted',
            'monthly_income_before', 'monthly_income_after',
            'other_significant_changes', 'remarks', 'department_unit',
            'contact_person', 'contact_number_email',
            # This is the line that was missing!
            'supporting_documents', 
        )
        widgets = {
            'date_started': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
            'other_significant_changes': forms.Textarea(attrs={'rows': 3}),
            'projects_involved': forms.Textarea(attrs={'rows': 3}),
            'trainings_attended': forms.Textarea(attrs={'rows': 3}),
            'other_assistance_received': forms.Textarea(attrs={'rows': 3}),
            'technologies_adopted': forms.Textarea(attrs={'rows': 3}),
            'adopter_address': forms.Textarea(attrs={'rows': 2}),
        }

class Table6Form(forms.ModelForm):
    class Meta:
        model = Table6IEC
        fields = (
            'no', 'code', 'related_curricular_offering', 'title', 'format',
            'male_recipients', 'female_recipients', 'student_recipients',
            'farmer_recipients', 'fisherfolk_recipients', 'ag_technician_recipients',
            'gov_employee_recipients', 
            'priv_employee_recipients',
            'other_recipients',
            'project_no', 'sdg', 'thematic_area',
            'remarks', 'department_unit', 'contact_person',
            'contact_number_email', 'supporting_documents'
        )
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7aForm(forms.ModelForm):
    class Meta:
        model = Table7aBudgetGAA
        fields = (
            'no', 'total_budget_allocated', 'department', 'curricular_offering',
            'allocated_budget', 'amount_utilized', 'remarks', 'supporting_documents'
        )
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7bForm(forms.ModelForm):
    class Meta:
        model = Table7bBudgetIncome
        fields = (
            'no', 'total_budget_allocated', 'department', 'curricular_offering',
            'allocated_budget', 'amount_utilized', 'remarks', 'supporting_documents'
        )
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
