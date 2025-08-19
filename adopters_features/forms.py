from django import forms
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

class Table5Form(forms.ModelForm):
    class Meta:
        model = Table5Adopter
        exclude = ('submission', 'income_difference', 'lead_unit')
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
        exclude = ('submission', 'total_recipients', 'lead_unit')
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7aForm(forms.ModelForm):
    class Meta:
        model = Table7aBudgetGAA
        exclude = ('submission',)
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7bForm(forms.ModelForm):
    class Meta:
        model = Table7bBudgetIncome
        exclude = ('submission',)
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
