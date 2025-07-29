from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse # Import HttpResponse for CSV export
import csv # Import the csv module

from .forms import ExtensionPPAFeaturedForm
from .models import ExtensionPPAFeatured, ExtensionPPA, MediaOutlet # Ensure all models are imported

def media_feature_form(request):
    """
    Handles the display and submission of the media feature form,
    and lists existing media feature records.
    """
    if request.method == 'POST':
        form = ExtensionPPAFeaturedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media feature record added successfully!')
            return redirect('media_feature_form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExtensionPPAFeaturedForm()

    # Get all existing records for display, ordered by date_featured descending
    # Use select_related to optimize database queries for related objects
    features = ExtensionPPAFeatured.objects.select_related(
        'extension_ppa', 'media_outlet'
    ).all().order_by('-date_featured') # Added ordering for consistent display

    context = {
        'form': form,
        'features': features
    }
    return render(request, 'media_features/feature_form.html', context)

def export_media_features_csv(request):
    """
    Exports all ExtensionPPAFeatured records to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    # Set the filename for the downloaded CSV file
    response['Content-Disposition'] = 'attachment; filename="media_features_export.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'PPA Title',
        'Media Type',
        'Media Outlet Name',
        'Date Featured',
        'Remarks'
    ])

    # Fetch all data, optimizing queries with select_related
    features = ExtensionPPAFeatured.objects.select_related(
        'extension_ppa', 'media_outlet'
    ).all().order_by('-date_featured') # Order consistent with display

    # Write data rows
    for feature in features:
        writer.writerow([
            feature.extension_ppa.ppa_name,
            feature.media_outlet.get_media_type_display(), # Use get_media_type_display for human-readable type
            feature.media_outlet.media_outlet_name,
            feature.date_featured.strftime('%Y-%m-%d'), # Format date as YYYY-MM-DD
            feature.remarks if feature.remarks else '' # Handle potential None for remarks
        ])

    return response

