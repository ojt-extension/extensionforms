from django import forms
from django.utils import timezone
from .models import ExtensionPPAFeatured, ExtensionPPA, MediaOutlet, Technology, Department, TechnologyStatus, CurricularOffering


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