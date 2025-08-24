# admin.py
from django.contrib import admin
from .models import (
    Partnership, InterFep, ExterFep, AdvServices, LeadUnit, PartnerAgencies,
    ProjectNoInText, CmmSrvy, IfpoProg, Proj, AwardRcvd, IfpoProgExter,
    ProjExter, AwardsRcvdExter, AdvSClients, AsTimeliness, EstExsFund,
    AsOverallRating, PartnershipFile, PartnershipImage, InterFepFile,
    InterFepImage, ExterFepFile, ExterFepImage, AdvServicesFile, AdvServicesImage
)

# Inline classes for file uploads
class PartnershipFileInline(admin.TabularInline):
    model = PartnershipFile
    extra = 0
    readonly_fields = ('uploaded_at',)

class PartnershipImageInline(admin.TabularInline):
    model = PartnershipImage
    extra = 0
    readonly_fields = ('uploaded_at',)

class InterFepFileInline(admin.TabularInline):
    model = InterFepFile
    extra = 0
    readonly_fields = ('uploaded_at',)

class InterFepImageInline(admin.TabularInline):
    model = InterFepImage
    extra = 0
    readonly_fields = ('uploaded_at',)

class ExterFepFileInline(admin.TabularInline):
    model = ExterFepFile
    extra = 0
    readonly_fields = ('uploaded_at',)

class ExterFepImageInline(admin.TabularInline):
    model = ExterFepImage
    extra = 0
    readonly_fields = ('uploaded_at',)

class AdvServicesFileInline(admin.TabularInline):
    model = AdvServicesFile
    extra = 0
    readonly_fields = ('uploaded_at',)

class AdvServicesImageInline(admin.TabularInline):
    model = AdvServicesImage
    extra = 0
    readonly_fields = ('uploaded_at',)

# Main model admins
@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ('partship_id', 'natpart', 'leadunit', 'partagency', 'datenotar')
    list_filter = ('natpart', 'themarea', 'level', 'catage')
    search_fields = ('categ', 'leadunit__department', 'partagency__nameagen')
    readonly_fields = ()
    inlines = [PartnershipFileInline, PartnershipImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('moano', 'code', 'categ', 'datenotar', 'natpart')
        }),
        ('Partnership Details', {
            'fields': ('leadunit', 'curricoff', 'numpart', 'partagency', 'level', 'catage')
        }),
        ('Project Information', {
            'fields': ('tappext', 'tofpart', 'dappbor', 'duration', 'incldate', 'amntinvlv')
        }),
        ('Classification', {
            'fields': ('sdgnum', 'themarea', 'extacperiod')
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

@admin.register(InterFep)
class InterFepAdmin(admin.ModelAdmin):
    list_display = ('interfepid', 'projno', 'lunitid', 'collabagenid', 'dateappborid')
    list_filter = ('themarea',)
    search_fields = ('lunitid__department', 'collabagenid__nameagen')
    readonly_fields = ()
    inlines = [InterFepFileInline, InterFepImageInline]
    
    fieldsets = (
        ('Project Information', {
            'fields': ('projno', 'code', 'lunitid', 'curricoffid', 'collabagenid')
        }),
        ('Project Details', {
            'fields': ('cmmsrvyid', 'ifpartofprogid', 'projid')
        }),
        ('Dates', {
            'fields': ('dateappborid',)
        }),
        ('Content', {
            'fields': ('sdgnum', 'themarea', 'awrdrcvdid')
        }),
        ('Partnership Link', {
            'fields': ('partship',)
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

@admin.register(ExterFep)
class ExterFepAdmin(admin.ModelAdmin):
    list_display = ('exterfep_id', 'projno', 'lunitid', 'collabgenid', 'dtappfagency')
    list_filter = ('themarea',)
    search_fields = ('lunitid__department', 'collabgenid__nameagen', 'fundagency')
    readonly_fields = ()
    inlines = [ExterFepFileInline, ExterFepImageInline]
    
    fieldsets = (
        ('Project Information', {
            'fields': ('projno', 'code', 'lunitid', 'curricoffid', 'collabgenid')
        }),
        ('External Funding', {
            'fields': ('fundagency', 'dtappfagency', 'dtinmeet')
        }),
        ('Project Details', {
            'fields': ('ifpoprogid', 'projid', 'awardrcvdid')
        }),
        ('Content', {
            'fields': ('sdgnum', 'themarea')
        }),
        ('Partnership Link', {
            'fields': ('partship',)
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

@admin.register(AdvServices)
class AdvServicesAdmin(admin.ModelAdmin):
    list_display = ('advservices_id', 'number', 'lunitid', 'collabagenciesid')
    list_filter = ('themarea',)
    search_fields = ('lunitid__department', 'collabagenciesid__nameagen', 'venue')
    readonly_fields = ()
    inlines = [AdvServicesFileInline, AdvServicesImageInline]
    
    fieldsets = (
        ('Service Information', {
            'fields': ('number', 'code', 'lunitid', 'curricoffid', 'collabagenciesid', 'clientsid')
        }),
        ('Service Details', {
            'fields': ('projno', 'adservprov', 'incldates', 'venue')
        }),
        ('Ratings', {
            'fields': ('adservoverall', 'adservtimeliness', 'totaladservreq', 'totaladservreqrespond')
        }),
        ('Funding', {
            'fields': ('estexsourcefund',)
        }),
        ('Classification', {
            'fields': ('sdgnum', 'themarea')
        }),
        ('Partnership Link', {
            'fields': ('partship',)
        }),
        ('Additional Information', {
            'fields': ('remarks',)
        }),
    )

# Supporting model admins
@admin.register(LeadUnit)
class LeadUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'contper')
    search_fields = ('department', 'contper')

@admin.register(PartnerAgencies)
class PartnerAgenciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nameagen', 'headagen')
    search_fields = ('nameagen', 'headagen')

@admin.register(ProjectNoInText)
class ProjectNoInTextAdmin(admin.ModelAdmin):
    list_display = ('project_no', 'proj_type')
    list_filter = ('proj_type',)

@admin.register(CmmSrvy)
class CmmSrvyAdmin(admin.ModelAdmin):
    list_display = ('cmmsrvyid', 'datecondt', 'datepresent', 'datercvd')
    list_filter = ('datecondt', 'datepresent')

@admin.register(IfpoProg)
class IfpoProgAdmin(admin.ModelAdmin):
    list_display = ('ifpoprogid', 'title', 'proglead', 'totalbudg')
    search_fields = ('title', 'proglead')

@admin.register(Proj)
class ProjAdmin(admin.ModelAdmin):
    list_display = ('projid', 'title', 'totalbudg')
    search_fields = ('title',)

@admin.register(AwardRcvd)
class AwardRcvdAdmin(admin.ModelAdmin):
    list_display = ('awardrcvd_id', 'titleaward', 'conferagn', 'date')
    search_fields = ('titleaward', 'conferagn')
    list_filter = ('date',)

@admin.register(IfpoProgExter)
class IfpoProgExterAdmin(admin.ModelAdmin):
    list_display = ('ifpoprogexter_id', 'title', 'proglead', 'tbudget')
    search_fields = ('title', 'proglead')

@admin.register(ProjExter)
class ProjExterAdmin(admin.ModelAdmin):
    list_display = ('projexter_id', 'title', 'tbudget')
    search_fields = ('title',)

@admin.register(AwardsRcvdExter)
class AwardsRcvdExterAdmin(admin.ModelAdmin):
    list_display = ('arexter_id', 'toaward', 'conferagency')
    search_fields = ('toaward', 'conferagency')

@admin.register(AdvSClients)
class AdvSClientsAdmin(admin.ModelAdmin):
    list_display = ('adsclients_id', 'name', 'organization', 'sex', 'categ')
    search_fields = ('name', 'organization')
    list_filter = ('sex', 'categ')

@admin.register(AsTimeliness)
class AsTimelinessAdmin(admin.ModelAdmin):
    list_display = ('astimeliness_id', 'one', 'two', 'three', 'four', 'five')

@admin.register(EstExsFund)
class EstExsFundAdmin(admin.ModelAdmin):
    list_display = ('estexsfund_id', 'amntchcvsu', 'amntchpartagency', 'partagencyname')
    search_fields = ('partagencyname',)

@admin.register(AsOverallRating)
class AsOverallRatingAdmin(admin.ModelAdmin):
    list_display = ('oallrate_id', 'one', 'two', 'three', 'four', 'five')

# File model admins (optional, for detailed file management)
@admin.register(PartnershipFile)
class PartnershipFileAdmin(admin.ModelAdmin):
    list_display = ('partnership', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(PartnershipImage)
class PartnershipImageAdmin(admin.ModelAdmin):
    list_display = ('partnership', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(InterFepFile)
class InterFepFileAdmin(admin.ModelAdmin):
    list_display = ('interfep', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(InterFepImage)
class InterFepImageAdmin(admin.ModelAdmin):
    list_display = ('interfep', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(ExterFepFile)
class ExterFepFileAdmin(admin.ModelAdmin):
    list_display = ('exterfep', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(ExterFepImage)
class ExterFepImageAdmin(admin.ModelAdmin):
    list_display = ('exterfep', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(AdvServicesFile)
class AdvServicesFileAdmin(admin.ModelAdmin):
    list_display = ('advservices', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

@admin.register(AdvServicesImage)
class AdvServicesImageAdmin(admin.ModelAdmin):
    list_display = ('advservices', 'filename', 'uploaded_at')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)