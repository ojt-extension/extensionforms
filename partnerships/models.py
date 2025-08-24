# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
import os

def upload_to_partnership(instance, filename):
    from django.utils.html import escape
    import os
    safe_filename = escape(os.path.basename(filename))
    return f'partnership/{instance.partnership.partship_id}/{safe_filename}'

def upload_to_interfep(instance, filename):
    from django.utils.html import escape
    import os
    safe_filename = escape(os.path.basename(filename))
    return f'interfep/{instance.interfep.interfepid}/{safe_filename}'

def upload_to_exterfep(instance, filename):
    from django.utils.html import escape
    import os
    safe_filename = escape(os.path.basename(filename))
    return f'exterfep/{instance.exterfep.exterfep_id}/{safe_filename}'

def upload_to_advservices(instance, filename):
    from django.utils.html import escape
    import os
    safe_filename = escape(os.path.basename(filename))
    return f'advservices/{instance.advservices.advservices_id}/{safe_filename}'

class LeadUnit(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    contper = models.CharField(max_length=150, blank=True, null=True)
    continf = models.CharField(max_length=175, blank=True, null=True)

    class Meta:
        db_table = 'leadunit'

    def __str__(self):
        return self.department if self.department else f"LeadUnit {self.id}"

class PartnerAgencies(models.Model):
    id = models.AutoField(primary_key=True)
    nameagen = models.CharField(max_length=150, blank=True, null=True)
    headagen = models.CharField(max_length=100, blank=True, null=True)
    contdet = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'partneragencies'

    def __str__(self):
        return self.nameagen if self.nameagen else f"Agency {self.id}"

class ProjectNoInText(models.Model):
    project_no = models.IntegerField(primary_key=True)
    proj_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'projectnointext'
    
    def __str__(self):
        return f"Project {self.project_no}" + (f" - {self.proj_type}" if self.proj_type else "")

    def __str__(self):
        return f"Project {self.project_no}"

class Partnership(models.Model):
    NATURE_CHOICES = [
        ('Internal', 'Internally Funded'),
        ('External', 'Externally Funded'),
        ('Both', 'Both Internal and External'),
        ('Advisory', 'Advisory Services'),
    ]

    partship_id = models.AutoField(primary_key=True)
    moano = models.CharField(max_length=50, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    categ = models.CharField(max_length=100, blank=True, null=True)
    datenotar = models.DateField(blank=True, null=True)
    leadunit = models.ForeignKey(LeadUnit, on_delete=models.SET_NULL, null=True, blank=True)
    curricoff = models.CharField(max_length=100, blank=True, null=True)
    numpart = models.IntegerField(blank=True, null=True)
    partagency = models.ForeignKey(PartnerAgencies, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=30, blank=True, null=True)
    catage = models.CharField(max_length=50, blank=True, null=True)
    natpart = models.CharField(max_length=100, choices=NATURE_CHOICES, blank=True, null=True)
    tappext = models.CharField(max_length=100, blank=True, null=True)
    tofpart = models.CharField(max_length=100, blank=True, null=True)
    dappbor = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    incldate = models.DateField(blank=True, null=True)
    amntinvlv = models.IntegerField(blank=True, null=True)
    sdgnum = models.CharField(max_length=70, blank=True, null=True)
    themarea = models.CharField(max_length=30, blank=True, null=True)
    extacperiod = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'partnership'

    def __str__(self):
        return f"Partnership {self.partship_id}"
    
    def get_available_form_types(self):
        """Get list of form types that can be created for this partnership"""
        form_types = []
        if self.natpart in ['Internal', 'Both']:
            form_types.append('internal')
        if self.natpart in ['External', 'Both']:
            form_types.append('external')
        if self.natpart == 'Advisory':
            form_types.append('advisory')
        return form_types
    
    def get_auto_population_data(self):
        """Get data for auto-populating related forms"""
        return {
            'leadunit': self.leadunit,
            'partagency': self.partagency,
            'curricoff': self.curricoff,
            'sdgnum': self.sdgnum,
            'themarea': self.themarea,
            'duration': self.duration,
            'incldate': self.incldate,
            'amntinvlv': self.amntinvlv,
        }
    
    def create_related_forms(self, form_types=None):
        """Create related forms based on partnership nature"""
        return AutoPopulationManager.auto_populate_forms(self, form_types)

class AutoPopulationManager:
    """
    Centralized manager for auto-population logic across all forms
    """
    
    @staticmethod
    def get_partnership_base_data(partnership):
        """Extract common data from partnership for auto-population"""
        if not partnership:
            return {}
        
        return {
            'leadunit': partnership.leadunit,
            'partagency': partnership.partagency,
            'curricoff': partnership.curricoff,
            'sdgnum': partnership.sdgnum,
            'themarea': partnership.themarea,
            'duration': partnership.duration,
            'incldate': partnership.incldate,
            'amntinvlv': partnership.amntinvlv,
        }
    
    @staticmethod
    def create_internal_project_template(partnership):
        """Create auto-populated internal project template"""
        if not partnership or partnership.natpart not in ['Internal', 'Both']:
            return None
        
        base_data = AutoPopulationManager.get_partnership_base_data(partnership)
        return {
            'partship': partnership,
            'lunitid': base_data.get('leadunit'),
            'collabagenid': base_data.get('partagency'),
            'curricoffid': base_data.get('curricoff'),
            'sdgnum': base_data.get('sdgnum'),
            'themarea': base_data.get('themarea'),
        }
    
    @staticmethod
    def create_external_project_template(partnership):
        """Create auto-populated external project template"""
        if not partnership or partnership.natpart not in ['External', 'Both']:
            return None
        
        base_data = AutoPopulationManager.get_partnership_base_data(partnership)
        return {
            'partship': partnership,
            'lunitid': base_data.get('leadunit'),
            'collabgenid': base_data.get('partagency'),
            'curricoffid': base_data.get('curricoff'),
            'sdgnum': base_data.get('sdgnum'),
            'themarea': base_data.get('themarea'),
        }
    
    @staticmethod
    def create_advisory_service_template(partnership):
        """Create auto-populated advisory service template"""
        if not partnership or partnership.natpart != 'Advisory':
            return None
        
        base_data = AutoPopulationManager.get_partnership_base_data(partnership)
        return {
            'partship': partnership,
            'lunitid': base_data.get('leadunit'),
            'collabagenciesid': base_data.get('partagency'),
            'curricoff': base_data.get('curricoff'),
            'sdgnum': base_data.get('sdgnum'),
            'themarea': base_data.get('themarea'),
        }
    
    @staticmethod
    def auto_populate_forms(partnership, form_types=None):
        """Auto-populate multiple form types based on partnership nature"""
        if not partnership:
            return {}
        
        results = {}
        
        # Determine which forms to create based on partnership nature
        if form_types is None:
            form_types = []
            if partnership.natpart in ['Internal', 'Both']:
                form_types.append('internal')
            if partnership.natpart in ['External', 'Both']:
                form_types.append('external')
            if partnership.natpart == 'Advisory':
                form_types.append('advisory')
        
        # Create templates for each form type
        for form_type in form_types:
            if form_type == 'internal':
                template = AutoPopulationManager.create_internal_project_template(partnership)
                if template:
                    results['internal'] = template
            elif form_type == 'external':
                template = AutoPopulationManager.create_external_project_template(partnership)
                if template:
                    results['external'] = template
            elif form_type == 'advisory':
                template = AutoPopulationManager.create_advisory_service_template(partnership)
                if template:
                    results['advisory'] = template
        
        return results

# Disabled automatic form creation - forms should be created manually by user
# @receiver(post_save, sender=Partnership)
# def auto_create_related_forms(sender, instance, created, **kwargs):
#     """DISABLED - Auto form creation moved to manual process"""
#     pass

# File upload models for Partnership
class PartnershipFile(models.Model):
    partnership = models.ForeignKey(Partnership, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_partnership)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.partnership.partship_id} - {self.filename}"

class PartnershipImage(models.Model):
    partnership = models.ForeignKey(Partnership, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_partnership)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.partnership.partship_id} - {self.filename}"

# Internal Projects Models
class CmmSrvy(models.Model):
    cmmsrvyid = models.AutoField(primary_key=True)
    datecondt = models.DateField(blank=True, null=True)
    dvstake = models.DateField(blank=True, null=True)
    datepresent = models.DateField(blank=True, null=True)
    datercvd = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'cmmsrvy'

class IfpoProg(models.Model):
    ifpoprogid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=190, blank=True, null=True)
    proglead = models.TextField(blank=True, null=True)
    apprvbudg = models.IntegerField(blank=True, null=True)
    cntptfund = models.IntegerField(blank=True, null=True)
    totalbudg = models.IntegerField(blank=True, null=True)
    incldateid = models.TextField(blank=True, null=True)
    moanoid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ifpoprog'

class Proj(models.Model):
    projid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90, blank=True, null=True)
    tmbrroles = models.TextField(blank=True, null=True)
    apprvbudg = models.IntegerField(blank=True, null=True)
    cntptfund = models.IntegerField(blank=True, null=True)
    totalbudg = models.IntegerField(blank=True, null=True)
    incldateid = models.TextField(blank=True, null=True)
    moanoid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'proj'

class AwardRcvd(models.Model):
    awardrcvd_id = models.AutoField(primary_key=True)
    titleaward = models.TextField(blank=True, null=True)
    conferagn = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'awardrcvd'

class InterFep(models.Model):
    interfepid = models.AutoField(primary_key=True)
    projno = models.ForeignKey(ProjectNoInText, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.IntegerField(blank=True, null=True)
    categid = models.CharField(max_length=15, blank=True, null=True)
    lunitid = models.ForeignKey(LeadUnit, on_delete=models.SET_NULL, null=True, blank=True)
    curricoffid = models.CharField(max_length=50, blank=True, null=True)
    collabagenid = models.ForeignKey(PartnerAgencies, on_delete=models.SET_NULL, null=True, blank=True)
    cmmsrvyid = models.ForeignKey(CmmSrvy, on_delete=models.SET_NULL, null=True, blank=True)
    ifpartofprogid = models.ForeignKey(IfpoProg, on_delete=models.SET_NULL, null=True, blank=True)
    projid = models.ForeignKey(Proj, on_delete=models.SET_NULL, null=True, blank=True)
    dateapprec = models.DateField(blank=True, null=True)
    dateappborid = models.DateField(blank=True, null=True)
    dateincep = models.DateField(blank=True, null=True)
    benef = models.TextField(blank=True, null=True)
    sdgnum = models.CharField(max_length=70, blank=True, null=True)
    themarea = models.CharField(max_length=20, blank=True, null=True)
    awrdrcvdid = models.ForeignKey(AwardRcvd, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    partship = models.ForeignKey(Partnership, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'interfep'

    def __str__(self):
        return f"Internal Project {self.interfepid}"
    
    def get_auto_population_data(self):
        """Get data for auto-populating forms from this internal project"""
        return {
            'lunitid': self.lunitid,
            'collabagenid': self.collabagenid,
            'curricoffid': self.curricoffid,
            'sdgnum': self.sdgnum,
            'themarea': self.themarea,
            'partship': self.partship,
        }

# File upload models for Internal Projects
class InterFepFile(models.Model):
    interfep = models.ForeignKey(InterFep, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_interfep)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InterFepImage(models.Model):
    interfep = models.ForeignKey(InterFep, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_interfep)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# External Projects Models
class IfpoProgExter(models.Model):
    ifpoprogexter_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    proglead = models.CharField(max_length=50, blank=True, null=True)
    abfundagency = models.IntegerField(blank=True, null=True)
    cpfundcvsu = models.IntegerField(blank=True, null=True)
    tbudget = models.IntegerField(blank=True, null=True)
    incldates = models.TextField(blank=True, null=True)
    moano_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ifpoprogexter'

class ProjExter(models.Model):
    projexter_id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    tmembers = models.TextField(blank=True, null=True)
    abfundagency = models.IntegerField(blank=True, null=True)
    cpfundcvsu = models.IntegerField(blank=True, null=True)
    tbudget = models.IntegerField(blank=True, null=True)
    incldates = models.TextField(blank=True, null=True)
    moano_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'projexter'

class AwardsRcvdExter(models.Model):
    arexter_id = models.AutoField(primary_key=True)
    toaward = models.TextField(blank=True, null=True)
    conferagency = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'awardsrcvdexter'

class ExterFep(models.Model):
    exterfep_id = models.AutoField(primary_key=True)
    projno = models.ForeignKey(ProjectNoInText, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.IntegerField(blank=True, null=True)
    categid = models.CharField(max_length=15, blank=True, null=True)
    lunitid = models.ForeignKey(LeadUnit, on_delete=models.SET_NULL, null=True, blank=True)
    curricoffid = models.CharField(max_length=50, blank=True, null=True)
    collabgenid = models.ForeignKey(PartnerAgencies, on_delete=models.SET_NULL, null=True, blank=True)
    ifpoprogid = models.ForeignKey(IfpoProgExter, on_delete=models.SET_NULL, null=True, blank=True)
    projid = models.ForeignKey(ProjExter, on_delete=models.SET_NULL, null=True, blank=True)
    fundagency = models.CharField(max_length=150, blank=True, null=True)
    dtappfagency = models.DateField(blank=True, null=True)
    dtinmeet = models.DateField(blank=True, null=True)
    benef = models.TextField(blank=True, null=True)
    sdgnum = models.CharField(max_length=70, blank=True, null=True)
    themarea = models.CharField(max_length=20, blank=True, null=True)
    awardrcvdid = models.ForeignKey(AwardsRcvdExter, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    partship = models.ForeignKey(Partnership, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        db_table = 'exterfep'

    def __str__(self):
        return f"External Project {self.exterfep_id}"
    
    def get_auto_population_data(self):
        """Get data for auto-populating forms from this external project"""
        return {
            'lunitid': self.lunitid,
            'collabgenid': self.collabgenid,
            'curricoffid': self.curricoffid,
            'sdgnum': self.sdgnum,
            'themarea': self.themarea,
            'partship': self.partship,
        }

# File upload models for External Projects
class ExterFepFile(models.Model):
    exterfep = models.ForeignKey(ExterFep, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_exterfep)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExterFepImage(models.Model):
    exterfep = models.ForeignKey(ExterFep, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_exterfep)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Advisory Services Models
class AdvSClients(models.Model):
    adsclients_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    organization = models.TextField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    categ = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'advsclients'

class AsTimeliness(models.Model):
    astimeliness_id = models.AutoField(primary_key=True)
    one = models.IntegerField(blank=True, null=True)
    two = models.IntegerField(blank=True, null=True)
    three = models.IntegerField(blank=True, null=True)
    four = models.IntegerField(blank=True, null=True)
    five = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'astimeliness'

class EstExsFund(models.Model):
    estexsfund_id = models.AutoField(primary_key=True)
    amntchcvsu = models.IntegerField(blank=True, null=True)
    amntchpartagency = models.IntegerField(blank=True, null=True)
    partagencyname = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'estexsfund'

class AsOverallRating(models.Model):
    oallrate_id = models.AutoField(primary_key=True)
    one = models.IntegerField(blank=True, null=True)
    two = models.IntegerField(blank=True, null=True)
    three = models.IntegerField(blank=True, null=True)
    four = models.IntegerField(blank=True, null=True)
    five = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'asoverallrating'

class AdvServices(models.Model):
    advservices_id = models.AutoField(primary_key=True)
    number = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    lunitid = models.ForeignKey(LeadUnit, on_delete=models.SET_NULL, null=True, blank=True)
    curricoff = models.CharField(max_length=100, blank=True, null=True , verbose_name="Curriculum Offered")
    collabagenciesid = models.ForeignKey(PartnerAgencies, on_delete=models.SET_NULL, null=True, blank=True)
    clientsid = models.ForeignKey(AdvSClients, on_delete=models.SET_NULL, null=True, blank=True)
    projno = models.ForeignKey(ProjectNoInText, on_delete=models.SET_NULL, null=True, blank=True)
    adservprov = models.TextField(blank=True, null=True)
    incldates = models.TextField(blank=True, null=True)
    venue = models.TextField(blank=True, null=True)
    adservoverall = models.ForeignKey(AsOverallRating, on_delete=models.SET_NULL, null=True, blank=True)
    adservtimeliness = models.ForeignKey(AsTimeliness, on_delete=models.SET_NULL, null=True, blank=True)
    totaladservreq = models.IntegerField(blank=True, null=True)
    totaladservreqrespond = models.IntegerField(blank=True, null=True)
    estexsourcefund = models.ForeignKey(EstExsFund, on_delete=models.SET_NULL, null=True, blank=True)
    sdgnum = models.CharField(max_length=70, blank=True, null=True)
    themarea = models.CharField(max_length=30, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    partship = models.ForeignKey(Partnership, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        db_table = 'advservices'

    def __str__(self):
        return f"Advisory Service {self.advservices_id}"
    
    def get_auto_population_data(self):
        """Get data for auto-populating forms from this advisory service"""
        return {
            'lunitid': self.lunitid,
            'collabagenciesid': self.collabagenciesid,
            'curricoff': self.curricoff,
            'sdgnum': self.sdgnum,
            'themarea': self.themarea,
            'partship': self.partship,
        }

# File upload models for Advisory Services
class AdvServicesFile(models.Model):
    advservices = models.ForeignKey(AdvServices, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_advservices)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AdvServicesImage(models.Model):
    advservices = models.ForeignKey(AdvServices, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_advservices)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now=True)

