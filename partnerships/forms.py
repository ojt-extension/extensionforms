# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (
    Partnership, InterFep, ExterFep, AdvServices, LeadUnit, PartnerAgencies,
    ProjectNoInText, CmmSrvy, IfpoProg, Proj, AwardRcvd
)
from .mixins import FileValidationMixin
from typing import Any, List, Tuple

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = []
            for d in data:
                try:
                    result.append(single_file_clean(d, initial))
                except forms.ValidationError as e:
                    raise forms.ValidationError(f"File validation error: {e}")
        else:
            result = single_file_clean(data, initial)
        return result

class PartnershipForm(FileValidationMixin, forms.ModelForm):
    files = MultipleFileField(required=False, help_text="Upload up to 10 files")
    images = MultipleFileField(required=False, help_text="Upload up to 10 images")

    # Sub-field fields for LeadUnit
    leadunit_department = forms.CharField(required=False, max_length=150, label="Department")
    leadunit_contper = forms.CharField(required=False, max_length=150, label="Contact Person")
    leadunit_continf = forms.CharField(required=False, max_length=175, label="Contact Information")
    
    # Sub-field fields for PartnerAgencies
    partagency_name = forms.CharField(required=False, max_length=150, label="Agency Name")
    
    class Meta:
        model = Partnership
        fields = [
            'moano', 'code', 'categ', 'datenotar', 'leadunit', 'curricoff', 'numpart',
            'partagency', 'level', 'catage', 'natpart', 'tappext', 'tofpart', 'dappbor',
            'duration', 'incldate', 'amntinvlv', 'sdgnum', 'themarea', 'extacperiod', 'remarks'
        ]
        widgets = {
            'moano': forms.NumberInput(attrs={'placeholder': 'Enter MOA number'}),
            'code': forms.NumberInput(attrs={'placeholder': 'Enter code(c/o Extension Services)'}),
            'categ': forms.TextInput(attrs={'placeholder': 'Enter category (New, Existing; On process)', 'maxlength': '50'}),
            'datenotar': forms.DateInput(attrs={'type': 'date'}),
            'curricoff': forms.TextInput(attrs={'placeholder': 'Enter curriculum offering (e.g. Bs Agriculture)', 'maxlength': '50'}),
            'numpart': forms.NumberInput(attrs={'placeholder': 'Enter number of partner agencies'}),
            'level': forms.TextInput(attrs={'placeholder': 'Enter Level (Local, Regional, National or International)', 'maxlength': '30'}),
            'catage': forms.TextInput(attrs={'placeholder': 'Enter Category of Agency (Government, NGO, Private or MSME)', 'maxlength': '50'}),
            'natpart': forms.Select(choices=Partnership.NATURE_CHOICES),
            'tappext': forms.TextInput(attrs={'placeholder': 'Enter application extension type (Indicate NA if no related approved extension program/project/activity)', 'maxlength': '100'}),
            'tofpart': forms.TextInput(attrs={'placeholder': 'Enter type of partnership (MOA, MOU or LOA)', 'maxlength': '10'}),
            'dappbor': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Enter duration (Number of years/months)', 'maxlength': '100'}),
            'incldate': forms.DateInput(attrs={'type': 'date'}),
            'amntinvlv': forms.NumberInput(attrs={'placeholder': 'Enter amount involved (if there is any)'}),
            'sdgnum': forms.TextInput(attrs={'placeholder': 'Enter SDG number (Indicate Number/s)', 'maxlength': '70'}),
            'themarea': forms.TextInput(attrs={'placeholder': 'Enter thematic area (A: Agri-Fisheries, B: Biodiversity, C: Smart Engineering, D: Public Health, E: Societal Development)', 'maxlength': '20'}),
            'extacperiod': forms.Textarea(attrs={'placeholder': 'Enter extension activity period (indicate dates and activities conducted within the period)', 'rows': 3}),
            'remarks': forms.Textarea(attrs={'placeholder': 'Enter remarks', 'maxlength': '200', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the foreign key fields since we use sub-fields
        if 'leadunit' in self.fields:
            self.fields['leadunit'].widget = forms.HiddenInput()
            self.fields['leadunit'].required = False
        if 'partagency' in self.fields:
            self.fields['partagency'].widget = forms.HiddenInput()
            self.fields['partagency'].required = False

    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images

class InterFepForm(FileValidationMixin, forms.ModelForm):
    files = MultipleFileField(required=False, help_text="Upload up to 10 files")
    images = MultipleFileField(required=False, help_text="Upload up to 10 images")
    
    # Override projno to be a text input instead of ModelChoiceField
    projno = forms.CharField(required=False, label="Project Number", widget=forms.TextInput(attrs={'placeholder': 'Enter project number'}))

    # Sub-field fields for LeadUnit
    lunit_department = forms.CharField(required=False, max_length=150, label="Department")
    lunit_contper = forms.CharField(required=False, max_length=150, label="Contact Person")
    lunit_continf = forms.CharField(required=False, max_length=175, label="Contact Information")
    
    # Sub-field fields for Collaborating Agency
    collab_name = forms.CharField(required=False, max_length=150, label="Agency Name")
    
    # Sub-field fields for Community Survey
    cmm_datecondt = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Conducted")
    cmm_dvstake = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Stakeholder Meeting")
    cmm_datepresent = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Presented")
    cmm_datercvd = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Received")
    
    # Sub-field fields for Program
    prog_title = forms.CharField(required=False, max_length=190, label="Program Title")
    prog_lead = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Program Lead")
    prog_apprvbudg = forms.IntegerField(required=False, label="Approved Budget")
    prog_cntptfund = forms.IntegerField(required=False, label="Counterpart Fund")
    prog_totalbudg = forms.IntegerField(required=False, label="Total Budget")
    prog_incldateid = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Inclusive Dates")
    
    # Sub-field fields for Project
    proj_title = forms.CharField(required=False, max_length=90, label="Project Title")
    proj_tmbrroles = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Team Member Roles")
    proj_apprvbudg = forms.IntegerField(required=False, label="Approved Budget")
    proj_cntptfund = forms.IntegerField(required=False, label="Counterpart Fund")
    proj_totalbudg = forms.IntegerField(required=False, label="Total Budget")
    proj_incldateid = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Inclusive Dates")
    
    # Sub-field fields for Award Received
    award_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Award Title")
    award_conferagn = forms.CharField(required=False, max_length=200, label="Conferring Agency")
    award_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date Received")

    class Meta:
        model = InterFep
        fields = [
            'code', 'categid', 'lunitid', 'curricoffid', 'collabagenid',
            'cmmsrvyid', 'ifpartofprogid', 'projid', 'dateapprec', 'dateappborid', 'dateincep',
            'benef', 'sdgnum', 'themarea', 'awrdrcvdid', 'remarks', 'partship'
        ]
        widgets = {
            'dateapprec': forms.DateInput(attrs={'type': 'date'}),
            'dateappborid': forms.DateInput(attrs={'type': 'date'}),
            'dateincep': forms.DateInput(attrs={'type': 'date'}),
            'benef': forms.Textarea(attrs={'rows': 3}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        partnership_id = kwargs.pop('partnership_id', None)
        super().__init__(*args, **kwargs)
        
        # Hide the original single fields since we're using sub-fields, but keep them for saving
        hidden_fields = ['lunitid', 'collabagenid', 'cmmsrvyid', 'ifpartofprogid', 'projid', 'awrdrcvdid']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False
        
        # projno is now a CharField, no queryset needed

        # Filter partnerships for Internal or Both types only
        self.fields['partship'].queryset = Partnership.objects.filter(natpart__in=['Internal', 'Both'])
        if partnership_id:
            self.fields['partship'].initial = partnership_id
        
        # Make partnership field optional
        self.fields['partship'].required = False

    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images

class ExterFepForm(FileValidationMixin, forms.ModelForm):
    files = MultipleFileField(required=False, help_text="Upload up to 10 files")
    images = MultipleFileField(required=False, help_text="Upload up to 10 images")
    
    # Override projno to be a text input instead of ModelChoiceField
    projno = forms.CharField(required=False, label="Project Number", widget=forms.TextInput(attrs={'placeholder': 'Enter project number'}))

    # Sub-field fields for LeadUnit
    lunit_department = forms.CharField(required=False, max_length=150, label="Department")
    lunit_contper = forms.CharField(required=False, max_length=150, label="Contact Person")
    lunit_continf = forms.CharField(required=False, max_length=175, label="Contact Information")
    
    # Sub-field fields for Collaborating Agency
    collab_name = forms.CharField(required=False, max_length=150, label="Agency Name")
    
    # Sub-field fields for External Program
    extprog_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Program Title")
    extprog_proglead = forms.CharField(required=False, max_length=50, label="Program Lead")
    extprog_abfundagency = forms.IntegerField(required=False, label="Budget from Funding Agency")
    extprog_cpfundcvsu = forms.IntegerField(required=False, label="Counterpart Fund from CVSU")
    extprog_tbudget = forms.IntegerField(required=False, label="Total Budget")
    extprog_incldates = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Inclusive Dates")
    
    # Sub-field fields for External Project
    extproj_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Project Title")
    extproj_tmembers = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Team Members")
    extproj_abfundagency = forms.IntegerField(required=False, label="Budget from Funding Agency")
    extproj_cpfundcvsu = forms.IntegerField(required=False, label="Counterpart Fund from CVSU")
    extproj_tbudget = forms.IntegerField(required=False, label="Total Budget")
    extproj_incldates = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Inclusive Dates")
    
    # Sub-field fields for External Award
    extaward_toaward = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Award Title")
    extaward_conferagency = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Conferring Agency")
    extaward_date = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Date Received")

    class Meta:
        model = ExterFep
        fields = [
            'code', 'categid', 'lunitid', 'curricoffid', 'collabgenid',
            'ifpoprogid', 'projid', 'fundagency', 'dtappfagency', 'dtinmeet',
            'benef', 'sdgnum', 'themarea', 'awardrcvdid', 'remarks', 'partship'
        ]
        widgets = {
            'dtappfagency': forms.DateInput(attrs={'type': 'date'}),
            'dtinmeet': forms.DateInput(attrs={'type': 'date'}),
            'benef': forms.Textarea(attrs={'rows': 3}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        partnership_id = kwargs.pop('partnership_id', None)
        super().__init__(*args, **kwargs)
        
        # Hide the original single fields since we're using sub-fields, but keep them for saving
        hidden_fields = ['lunitid', 'collabgenid', 'ifpoprogid', 'projid', 'awardrcvdid']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False
        
        # projno is now a CharField, no queryset needed
        
        # Filter partnerships for External or Both types only
        self.fields['partship'].queryset = Partnership.objects.filter(natpart__in=['External', 'Both'])
        if partnership_id:
            self.fields['partship'].initial = partnership_id
        
        # Make partnership field optional
        self.fields['partship'].required = False

    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images

class AdvServicesForm(FileValidationMixin, forms.ModelForm):
    files = MultipleFileField(required=False, help_text="Upload up to 10 files")
    images = MultipleFileField(required=False, help_text="Upload up to 10 images")
    
    def __init__(self, *args, **kwargs):
        partnership_id = kwargs.pop('partnership_id', None)
        super().__init__(*args, **kwargs)
        
        # Keep the original model fields but make them hidden since we use sub-fields
        hidden_fields = ['lunitid', 'collabagenciesid', 'clientsid', 'adservoverall', 'adservtimeliness', 'estexsourcefund']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False
        
        # Ensure projno field is available
        if 'projno' in self.fields:
            self.fields['projno'].queryset = ProjectNoInText.objects.all()
            self.fields['projno'].required = False
        
        # Filter partnerships for Advisory type only
        self.fields['partship'].queryset = Partnership.objects.filter(natpart='Advisory')
        if partnership_id:
            self.fields['partship'].initial = partnership_id
            
        # Make partnership field optional
        self.fields['partship'].required = False

    # Sub-field fields for LeadUnit
    lunit_department = forms.CharField(required=False, max_length=150, label="Department")
    lunit_contper = forms.CharField(required=False, max_length=150, label="Contact Person")
    lunit_continf = forms.CharField(required=False, max_length=175, label="Contact Information")
    
    # Sub-field fields for Collaborating Agency
    collab_name = forms.CharField(required=False, max_length=150, label="Agency Name")
    collab_head = forms.CharField(required=False, max_length=100, label="Agency Head")
    collab_contact = forms.CharField(required=False, max_length=200, label="Contact Details")
    
    # Sub-field fields for Clients
    client_name = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Client Name")
    client_organization = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Organization")
    client_sex = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Sex")
    client_categ = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label="Category")
    client_number = forms.CharField(required=False, max_length=100, label="Number/Email")
    
    # Sub-field fields for Overall Rating
    overall_one = forms.IntegerField(required=False, label="Rating 1", min_value=0)
    overall_two = forms.IntegerField(required=False, label="Rating 2", min_value=0)
    overall_three = forms.IntegerField(required=False, label="Rating 3", min_value=0)
    overall_four = forms.IntegerField(required=False, label="Rating 4", min_value=0)
    overall_five = forms.IntegerField(required=False, label="Rating 5", min_value=0)
    
    # Sub-field fields for Timeliness Rating
    timeliness_one = forms.IntegerField(required=False, label="Rating 1", min_value=0)
    timeliness_two = forms.IntegerField(required=False, label="Rating 2", min_value=0)
    timeliness_three = forms.IntegerField(required=False, label="Rating 3", min_value=0)
    timeliness_four = forms.IntegerField(required=False, label="Rating 4", min_value=0)
    timeliness_five = forms.IntegerField(required=False, label="Rating 5", min_value=0)
    
    # Sub-field fields for External Source Fund
    fund_amntchcvsu = forms.IntegerField(required=False, label="Amount Charged to CVSU", min_value=0)
    fund_amntchpartagency = forms.IntegerField(required=False, label="Amount Charged to Partner Agency", min_value=0)
    fund_partagencyname = forms.CharField(required=False, max_length=150, label="Partner Agency Name")

    class Meta:
        model = AdvServices
        fields = [
            'number', 'code', 'lunitid', 'curricoff', 'collabagenciesid', 'clientsid',
            'projno', 'adservprov', 'incldates', 'venue', 'adservoverall',
            'adservtimeliness', 'totaladservreq', 'totaladservreqrespond',
            'estexsourcefund', 'sdgnum', 'themarea', 'remarks', 'partship'
        ]
        widgets = {
            'adservprov': forms.Textarea(attrs={'rows': 3}),
            'incldates': forms.Textarea(attrs={'rows': 2}),
            'venue': forms.Textarea(attrs={'rows': 2}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }



    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images

# Additional forms for related models
class LeadUnitForm(forms.ModelForm):
    class Meta:
        model = LeadUnit
        fields = '__all__'

class PartnerAgenciesForm(forms.ModelForm):
    class Meta:
        model = PartnerAgencies
        fields = '__all__'

class ProjectNoInTextForm(forms.ModelForm):
    class Meta:
        model = ProjectNoInText
        fields = '__all__'

class CmmSrvyForm(forms.ModelForm):
    class Meta:
        model = CmmSrvy
        fields = '__all__'
        widgets = {
            'datecondt': forms.DateInput(attrs={'type': 'date'}),
            'dvstake': forms.DateInput(attrs={'type': 'date'}),
            'datepresent': forms.DateInput(attrs={'type': 'date'}),
            'datercvd': forms.DateInput(attrs={'type': 'date'}),
        }

class IfpoProgForm(forms.ModelForm):
    class Meta:
        model = IfpoProg
        fields = '__all__'

class ProjForm(FileValidationMixin, forms.ModelForm):
    files = MultipleFileField(required=False, help_text="Upload up to 10 files")
    images = MultipleFileField(required=False, help_text="Upload up to 10 images")

    class Meta:
        model = Proj
        fields = '__all__'
        widgets = {
            'datecondt': forms.DateInput(attrs={'type': 'date'}),
            'dvstake': forms.DateInput(attrs={'type': 'date'}),
            'datepresent': forms.DateInput(attrs={'type': 'date'}),
            'datercvd': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_files(self):
        files = self.cleaned_data.get('files')
        if files and len(files) > 10:
            raise forms.ValidationError("Maximum 10 files allowed")
        return files

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images and len(images) > 10:
            raise forms.ValidationError("Maximum 10 images allowed")
        return images