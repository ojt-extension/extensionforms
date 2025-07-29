from django import forms
from django.utils import timezone
from .models import ExtensionPPAFeatured, ExtensionPPA, MediaOutlet


class ExtensionPPAFeaturedForm(forms.ModelForm):
    # Add a field to show existing PPAs
    existing_ppa = forms.ModelChoiceField(
        queryset=ExtensionPPA.objects.all(),
        required=False,
        empty_label="-- Select existing PPA or enter new below --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Custom field for PPA - allows creating new PPA on the fly
    ppa_name = forms.CharField(
        max_length=500,
        required=False,
        label="Or Enter New PPA Title",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new PPA title if not in list above'
        })
    )
    
    # Custom fields for Media Outlet
    media_type = forms.ChoiceField(
        choices=MediaOutlet._meta.get_field('media_type').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    media_outlet_name = forms.CharField(
        max_length=255,
        label="Media Outlet Name",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g., Philippine Daily Inquirer, GMA News Online'
        })
    )
    
    class Meta:
        model = ExtensionPPAFeatured
        fields = ['date_featured', 'remarks']
        widgets = {
            'date_featured': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Additional notes or comments (optional)'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        existing_ppa = cleaned_data.get('existing_ppa')
        ppa_name = cleaned_data.get('ppa_name')
        
        if not existing_ppa and not ppa_name:
            raise forms.ValidationError("Please select an existing PPA or enter a new one.")
        
        return cleaned_data
    
    def clean_date_featured(self):
        date = self.cleaned_data['date_featured']
        if date > timezone.now().date():
            raise forms.ValidationError("Date featured cannot be in the future.")
        return date
    
    def save(self, commit=True):
        # Use existing PPA if selected, otherwise create new
        if self.cleaned_data.get('existing_ppa'):
            ppa = self.cleaned_data['existing_ppa']
        else:
            ppa, _ = ExtensionPPA.objects.get_or_create(
                ppa_name=self.cleaned_data['ppa_name']
            )
        
        # Get or create the Media Outlet
        media_outlet, _ = MediaOutlet.objects.get_or_create(
            media_outlet_name=self.cleaned_data['media_outlet_name'],
            media_type=self.cleaned_data['media_type']
        )
        
        # Create the feature record
        instance = super().save(commit=False)
        instance.extension_ppa = ppa
        instance.media_outlet = media_outlet
        
        if commit:
            instance.save()
        return instance