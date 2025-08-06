# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse

from openpyxl import Workbook 
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

from django.db import transaction 

from .forms import ExtensionPPAFeaturedForm, TechnologyForm # <-- ADD TechnologyForm
from .models import ExtensionPPAFeatured, ExtensionPPA, MediaOutlet, SupportingDocument
from .models import Technology, Department, CurricularOffering

# from your_app_name.models import TechnologyCommercialized # Example for Table 11

def reports_dashboard(request):
    """
    Renders the main dashboard page with links to all forms.
    """
    forms = [
        {'name': 'Table 10: ES Activities Featured Forms', 'url_name': 'table_10_form'},
        # Add a dictionary for each of your 15 other forms here
        {'name': 'Table 11: Technologies Commercialized', 'url_name': 'table_11_form'},
    ]
    return render(request, 'media_features/dashboard.html', {'forms': forms})


def media_feature_form(request):
    """
    Handles the display and submission of the media feature form.
    """
    if request.method == 'POST':
        form = ExtensionPPAFeaturedForm(request.POST, request.FILES)
        if form.is_valid():
            
            with transaction.atomic():
                # Get the existing PPA or create a new one
                existing_ppa = form.cleaned_data.get('extension_ppa')
                new_ppa_name = form.cleaned_data.get('ppa_name')
                
                if new_ppa_name:
                    ppa_instance, created = ExtensionPPA.objects.get_or_create(ppa_name=new_ppa_name)
                else:
                    ppa_instance = existing_ppa

                # Find or create the MediaOutlet object
                media_outlet_name = form.cleaned_data.get('media_outlet_name')
                media_outlet_instance = None
                if media_outlet_name:
                    media_outlet_instance, created = MediaOutlet.objects.get_or_create(media_outlet_name=media_outlet_name)
                
                # Save the form instance and link the related objects
                feature_instance = form.save(commit=False)
                feature_instance.extension_ppa = ppa_instance
                feature_instance.media_outlet = media_outlet_instance
                feature_instance.save()

                # Handle multiple file uploads
                files = request.FILES.getlist('files')
                for file in files:
                    SupportingDocument.objects.create(extension_ppa_featured=feature_instance, file=file)
            
            messages.success(request, 'Media feature record and documents added successfully!')
            return redirect('table_10_form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExtensionPPAFeaturedForm()
    
    media_features = ExtensionPPAFeatured.objects.select_related('extension_ppa', 'media_outlet').prefetch_related('supporting_documents').all().order_by('-date_featured')

    context = {
        'form': form,
        'media_features': media_features
    }
    return render(request, 'media_features/table_10_form.html', context)

def technology_commercialized_form(request):
    """
    Handles the display and submission of the technologies commercialized form.
    """
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            technology_instance = form.save()
            
            # Handle multiple file uploads
            files = request.FILES.getlist('files')
            for file in files:
                SupportingDocument.objects.create(technology=technology_instance, file=file)
            
            messages.success(request, 'Technology record and documents added successfully!')
            return redirect('table_11_form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TechnologyForm()
    
    technologies = Technology.objects.select_related('department').prefetch_related('curricular_offerings', 'supporting_documents').all().order_by('-year_developed')
    
    context = {
        'form': form,
        'technologies': technologies
    }
    return render(request, 'media_features/table_11_form.html', context)

def get_curricular_offerings(request, department_id):
    """
    Returns a JSON response of curricular offerings for a given department.
    """
    offerings = CurricularOffering.objects.filter(department_id=department_id).values('curricular_offering_id', 'offering_name')
    return JsonResponse(list(offerings), safe=False)


# NEW: This is the main, centralized export function

def export_all_to_excel(request):
    workbook = Workbook()
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=all_extension_reports.xlsx'

    # Get the base URL from the request object
    base_url = request.build_absolute_uri('/')[:-1]

    # CORRECTED: Use base_url to create absolute URLs
    ExtensionPPAFeatured.add_to_class(
        'supporting_documents_list',
        lambda self: ", ".join([f"{base_url}{doc.file.url}" for doc in self.supporting_documents.all()])
    )
    Technology.add_to_class(
        'supporting_documents_list',
        lambda self: ", ".join([f"{base_url}{doc.file.url}" for doc in self.supporting_documents.all()])
    )

    Technology.add_to_class(
        'curricular_offerings_list',
        lambda self: ", ".join([offering.offering_name for offering in self.curricular_offerings.all()])
    )

    tables = {
        'Table 10 - Media Features': {
            'model': ExtensionPPAFeatured,
            'fields': [
                'extension_ppa__ppa_name',
                'media_outlet__media_outlet_name',
                'date_featured',
                'remarks',
                'supporting_documents_list'
            ],
            'headers': [
                'Extension Program/Project/Activity (PPA)',
                'Print, radio, online media where Extension PPA was featured',
                'Date Featured',
                'Remarks',
                'Supporting Documents'
            ],
            'notes': [
                '', '', '', '',
                '*Copy of any evidence showing the Extension PPA was featured'
            ]
        },
        'Table 11 - Technologies': {
            'model': Technology,
            'fields': [
                'department__department_name',
                'technology_title',
                'year_developed',
                'technology_generator',
                'technology_status__status_name',
                'curricular_offerings_list',
                'remarks',
                'supporting_documents_list'
            ],
            'headers': [
                'Department',
                'Technology Title',
                'Year Developed',
                'Technology Generator',
                'Technology Status',
                'Related Curricular Offerings',
                'Remarks',
                'Supporting Documents'
            ],
            'notes': [
                '', '', '', '', '', '', '',
                '1. Photo and IEC material about the technology\n2. Documentation of deployment, commercialization, and pre-commercialization activities'
            ]
        },
    }

    if not tables:
        sheet = workbook.create_sheet(title='No Data')
        sheet['A1'] = 'No data available for export.'
    
    if 'Sheet' in workbook.sheetnames:
        workbook.remove(workbook['Sheet'])

    for sheet_name, table_info in tables.items():
        model = table_info['model']
        fields = table_info['fields']
        headers = table_info['headers']
        notes = table_info['notes']

        sheet = workbook.create_sheet(title=sheet_name)
        
        for col_num, header_text in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num, value=header_text)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(wrap_text=True, vertical='center')

        for col_num, note_text in enumerate(notes, 1):
            if note_text:
                cell = sheet.cell(row=2, column=col_num, value=note_text)
                cell.alignment = Alignment(wrap_text=True, vertical='top')

        sheet.row_dimensions[1].height = 40
        sheet.row_dimensions[2].height = 60
        
        queryset = model.objects.all()
        
        if hasattr(model, 'extension_ppa'):
            queryset = queryset.select_related('extension_ppa', 'media_outlet').prefetch_related('supporting_documents')
        if hasattr(model, 'department'):
            queryset = queryset.select_related('department', 'technology_status').prefetch_related('curricular_offerings', 'supporting_documents')
        
        start_row = 3
        for record in queryset:
            row_data = []
            for field in fields:
                if field == 'curricular_offerings_list':
                    value = record.curricular_offerings_list()
                elif field == 'supporting_documents_list':
                    value = record.supporting_documents_list()
                else:
                    value = record
                    for part in field.split('__'):
                        if hasattr(value, part):
                            value = getattr(value, part)
                            if callable(value):
                                value = value()
                        else:
                            value = ''
                row_data.append(value)
            
            for col_num, cell_value in enumerate(row_data, 1):
                cell = sheet.cell(row=start_row, column=col_num, value=cell_value)
                cell.alignment = Alignment(wrap_text=True)
            start_row += 1

    workbook.save(response)
    return response
