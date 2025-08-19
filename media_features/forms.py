#media_features/forms.py
from django import forms
from django.utils import timezone
from .models import ExtensionPPAFeatured, ExtensionPPA, MediaOutlet, StudentExtensionInvolvement, Technology, Department, TechnologyStatus, CurricularOffering, FacultyInvolvement, Ordinance, ImpactAssessment, Awards, OtherActivities


    
class ExtensionPPAFeaturedForm(forms.ModelForm):
    extension_ppa = forms.ModelChoiceField(
        queryset=ExtensionPPA.objects.all().order_by('ppa_name'),
        required=False,
        label="Existing Extension PPA",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ppa_name = forms.CharField(
        max_length=255,
        required=False,
        label="New PPA Name",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    # Use a single field for the media outlet name
    media_outlet_name = forms.CharField(
        max_length=255,
        required=False,
        label="Print, radio, online media where Extension PPA was featured",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = ExtensionPPAFeatured
        fields = [
            'extension_ppa',
            'ppa_name',
            'media_outlet_name',
            'date_featured',
            'remarks',
        ]
        widgets = {
            'date_featured': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_ppa = cleaned_data.get('extension_ppa')
        new_ppa_name = cleaned_data.get('ppa_name')

        if not existing_ppa and not new_ppa_name:
            raise forms.ValidationError(
                "You must either select an existing PPA or provide a new PPA name."
            )
        if existing_ppa and new_ppa_name:
            raise forms.ValidationError(
                "You cannot select an existing PPA and provide a new name at the same time."
            )
        return cleaned_data
    
    def clean_date_featured(self):
        date = self.cleaned_data['date_featured']
        if date > timezone.now().date():
            raise forms.ValidationError("Date featured cannot be in the future.")
        return date
    
    def save(self, commit=True):
        # Use existing PPA if selected, otherwise create new
        if self.cleaned_data.get('extension_ppa'):
            ppa = self.cleaned_data['extension_ppa']
        else:
            ppa, _ = ExtensionPPA.objects.get_or_create(
                ppa_name=self.cleaned_data['ppa_name']
            )
        
        # Get or create the Media Outlet using only the name
        # If media_type is not required in the model, this will work.
        media_outlet, _ = MediaOutlet.objects.get_or_create(
            media_outlet_name=self.cleaned_data['media_outlet_name'],
            # The media_type field is now removed, so the `get_or_create` will not try to use it.
            # If the media_type field in the MediaOutlet model is nullable, this is fine.
        )
        
        # Create the feature record
        instance = super().save(commit=False)
        instance.extension_ppa = ppa
        instance.media_outlet = media_outlet
       
        if commit:
            instance.save()
        return instance
    
class TechnologyForm(forms.ModelForm):
    curricular_offerings = forms.ModelMultipleChoiceField(
        queryset=CurricularOffering.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Related Curricular Offerings"
    )

    class Meta:
        model = Technology
        fields = [
            'department', 
            'curricular_offerings',
            'technology_title', 
            'year_developed', 
            'technology_generator', 
            'technology_status', 
            'remarks'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'technology_title': forms.TextInput(attrs={'class': 'form-input'}),
            'year_developed': forms.NumberInput(attrs={'class': 'form-input'}),
            'technology_generator': forms.TextInput(attrs={'class': 'form-input'}),
            'technology_status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m() # This handles the Many-to-Many relationship
        return instance

# Add this to your forms.py file
class StudentExtensionInvolvementForm(forms.ModelForm):
    class Meta:
        model = StudentExtensionInvolvement
        fields = [
            'department',
            'curricular_offering',
            'total_students_for_period',
            'students_involved_in_extension',
            'remarks'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select', 'id': 'id_department'}),
            'curricular_offering': forms.Select(attrs={'class': 'form-select', 'id': 'id_curricular_offering'}),
            'total_students_for_period': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'id': 'total_students'
            }),
            'students_involved_in_extension': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'id': 'students_involved'
            }),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially, show no curricular offerings
        self.fields['curricular_offering'].queryset = CurricularOffering.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['curricular_offering'].queryset = CurricularOffering.objects.filter(department_id=department_id).order_by('offering_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['curricular_offering'].queryset = self.instance.department.curricular_offerings.order_by('offering_name')

    def clean_students_involved_in_extension(self):
        total_students = self.cleaned_data.get('total_students_for_period')
        students_involved = self.cleaned_data.get('students_involved_in_extension')
        
        if total_students is not None and students_involved is not None:
            if students_involved > total_students:
                raise forms.ValidationError(
                    "Number of students involved cannot exceed total number of students."
                )
        
        return students_involved

    def clean_total_students_for_period(self):
        total_students = self.cleaned_data.get('total_students_for_period')
        if total_students is not None and total_students <= 0:
            raise forms.ValidationError("Total number of students must be greater than 0.")
        return total_students

class FacultyInvolvementForm(forms.ModelForm):
    """
    Form for Table 8: Faculty Involvement in ESCE.
    """

    class Meta:
        model = FacultyInvolvement
        fields = [
            'faculty_staff_name', 'academic_rank_position', 'employment_status',
            'avg_hours_per_week', 'total_hours_per_quarter', 'remarks'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply the correct CSS classes based on field type
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-textarea'})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'class': 'form-input'})
            else:
                # Default fallback
                field.widget.attrs.update({'class': 'form-input'})

class OrdinanceForm(forms.ModelForm):
    class Meta:
        model = Ordinance
        fields = [
            'department',
            'curricular_offering',
            'extension_ppa',
            'ordinance_title',
            'status', 
            'date_approved', 
            'remarks'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'curricular_offering': forms.Select(attrs={'class': 'form-select'}),
            'extension_ppa': forms.Select(attrs={'class': 'form-select'}),
            'ordinance_title': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_approved': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply the correct CSS classes based on field type
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-textarea'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-input'})

class ImpactAssessmentForm(forms.ModelForm):
    class Meta:
        model = ImpactAssessment
        fields = [
            'department',
            'curricular_offering',
            'extension_ppa_ia',
            'proponent_ias',
            'date_conducted',
            'remarks'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'curricular_offering': forms.Select(attrs={'class': 'form-select'}),
            'extension_ppa_ia': forms.Select(attrs={'class': 'form-select'}),
            'proponent_ias': forms.TextInput(attrs={'class': 'form-input'}),
            'date_conducted': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply the correct CSS classes based on field type
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-textarea'})

class AwardsForm(forms.ModelForm):
    class Meta:
        model = Awards
        fields = [
            'department',
            'person_received_award',
            'award_title',
            'award_donor',
            'level_of_award',
            'date_received',
            'remarks'
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'person_received_award': forms.TextInput(attrs={'class': 'form-input'}),
            'award_title': forms.TextInput(attrs={'class': 'form-input'}),
            'award_donor': forms.TextInput(attrs={'class': 'form-input'}),
            'level_of_award': forms.Select(attrs={'class': 'form-select'}),
            'date_received': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply the correct CSS classes based on field type
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-textarea'})
            
class OtherActivitiesForm(forms.ModelForm):
    class Meta:
        model = OtherActivities
        fields = [
            'date_conducted',
            'activity_title',
            'category',
            'participants',
            'purpose',
            'amount_spent',
            'source_of_funds',
            'remarks'
        ]
        widgets = {
            'date_conducted': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'activity_title': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'participants': forms.TextInput(attrs={'class': 'form-input'}),
            'purpose': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'amount_spent': forms.NumberInput(attrs={'class': 'form-input'}),
            'source_of_funds': forms.TextInput(attrs={'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply the correct CSS classes based on field type
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-textarea'})