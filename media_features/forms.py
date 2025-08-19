#media_features/forms.py
from django import forms
from django.forms import ClearableFileInput
from django.utils import timezone
from .models import (
    ExtensionPPAFeatured, ExtensionPPA, MediaOutlet, StudentExtensionInvolvement, 
    Technology, TechnologyStatus, FacultyInvolvement, Training, CollaboratingAgency, 
    Category, ThematicArea, Project, SupportingDocument, LeadUnit, Department, 
    CurricularOffering, ContactPerson, TrainingCollaboratingAgency
)


DAYS_TRAINED_CHOICES = (
    ('5 or more days', '5 or more days (x 2.00)'),
    ('3 to 4 days', '3 to 4 days (x 1.5)'),
    ('2 days', '2 days (x 1.25)'),
    ('1 day (8 hours)', '1 day (8 hours) (x 1.00)'),
    ('Less than 1 day or 8 hours', 'Less than 1 day or 8 hours (x 0.5)'),
)


class TrainingForm(forms.ModelForm):
    
    # This field handles the M2M relationship
    collaborating_agencies = forms.ModelMultipleChoiceField(
        queryset=CollaboratingAgency.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Collaborating Agency/ies"
    )
    
    contact_person_training_coordinator = forms.CharField(
        label='Contact Person (Training Coordinator)',
        max_length=100
    )
    training_no = forms.CharField(label='Training No.', max_length=100)
    Total_participants_by_sex_display = forms.IntegerField(label='Total', required=False, disabled=True)
    Total_participants_by_category_display = forms.IntegerField(label='Total', required=False, disabled=True)
    TotalNoOfPersonsTrained_display = forms.IntegerField(label='Total No. of Persons Trained', required=False, disabled=True)
    Number_of_days_trained_weight_display = forms.DecimalField(
        label='Number of days trained per weight of training',
        required=False,
        disabled=True
    )
    amount_charged_to_cvsu = forms.DecimalField(
        label='Amount charged to CvSU (campus/college/unit)',
        max_digits=10,
        decimal_places=2,
        required=False
    )
    amount_charged_to_partner = forms.DecimalField(
        label='Amount charged to partner agency (PhP)',
        help_text='(if there is no cash involve, include estimates/value)',
        max_digits=10,
        decimal_places=2,
        required=False
    )
    name_of_partner_agency = forms.CharField(
        label='Name of Partner Agency',
        max_length=255,
        required=False
    )
    class Meta:
        model = Training
        fields = [
            'training_no','Code', 'TitleOfTraining', 'project', 'department', 'contact_person',
            'contact_number_email', 'related_curricular_offering',
            'InclusiveDates', 'Venue', 'category', 'total_male', 'total_female',
            'total_prefer_no_to_say', 'student_count', 'farmer_count', 'fisherfolk_count',
            'ag_technician_count', 'government_employee_count', 'private_employee_count',
            'fourps_count', 'others_count', 'solo_parent_count', 'fourps_members_count',
            'pwd_count', 'type_of_disability', 
            'Number_of_days_trained', 'TotalNoOfTraineesSurveyed', 'ClientRatingRelevance',
            'ClientRatingQuality', 'ClientRatingTimeliness', 'TotalNumberofClientsRequestingTrainings',
            'TotalNumberofRequestsResponded', 'sustainable_development_goal', 'thematic_area',
            'remarks', 'supporting_document', 'collaborating_agencies',  
            'contact_person_training_coordinator','amount_charged_to_cvsu', 'amount_charged_to_partner',
            'name_of_partner_agency',
            # You must REMOVE the 'files' field from this list if your model doesn't have it
        ]

        widgets = {
            'Number_of_days_trained': forms.RadioSelect(choices=DAYS_TRAINED_CHOICES),
            'ClientRatingRelevance': forms.RadioSelect(choices=zip(range(1, 6), range(1, 6))),
            'ClientRatingQuality': forms.RadioSelect(choices=zip(range(1, 6), range(1, 6))),
            'ClientRatingTimeliness': forms.RadioSelect(choices=zip(range(1, 6), range(1, 6))),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate dynamic dropdowns
       
        self.fields['department'].queryset = Department.objects.all().order_by('department_name')
        self.fields['project'].queryset = Project.objects.all().order_by('project_no')
        self.fields['category'].queryset = Category.objects.all().order_by('category_code')
        self.fields['thematic_area'].queryset = ThematicArea.objects.all().order_by('area_code')
        self.fields['contact_person'].queryset = ContactPerson.objects.all().order_by('name')
        self.fields['related_curricular_offering'].queryset = CurricularOffering.objects.all().order_by('offering_name')



class FinancialContributionForm(forms.ModelForm):
    class Meta:
        model = TrainingCollaboratingAgency
        fields = ['agency', 'amount_charged_to_cvsu', 'amount_charged_to_partner']

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


