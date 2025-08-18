from django import forms
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

class DateInput(forms.DateInput):
    input_type = 'date'

class Table5Form(forms.ModelForm):
    class Meta:
        model = Table5Adopter
        fields = '__all__'
        widgets = {
            'date_started': DateInput(),
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
        fields = '__all__'
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7aForm(forms.ModelForm):
    class Meta:
        model = Table7aBudgetGAA
        fields = '__all__'
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

class Table7bForm(forms.ModelForm):
    class Meta:
        model = Table7bBudgetIncome
        fields = '__all__'
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
