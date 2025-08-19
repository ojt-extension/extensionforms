from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import Table5Form, Table6Form, Table7aForm, Table7bForm
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome, Submission
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# ------------- Dashboard -------------
def dashboard(request):
    return render(request, 'adopters_features/dashboard.html')

# ---------- Helpers (Excel) ----------
def queryset_to_sheet(ws, queryset, field_order=None, header_map=None):
    if field_order is None:
        model = queryset.model
        field_order = [f.name for f in model._meta.fields]

    headers = []
    for f in field_order:
        pretty = header_map.get(f, f.replace('_', ' ').title()) if header_map else f.replace('_', ' ').title()
        headers.append(pretty)
    ws.append(headers)

    for obj in queryset:
        row = [getattr(obj, f) for f in field_order]
        ws.append(row)

    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].auto_size = True

def wb_response(wb, filename):
    resp = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(resp)
    return resp

def handle_delete(request, pk, model_class, redirect_name):
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect(redirect_name)

# ---------- Table 5 ----------
def table5_view(request):
    if request.method == 'POST':
        form = Table5Form(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Submission object linked to the current user
            submission = Submission.objects.create(submitter=request.user)
            # Save the form data without committing to the database yet
            table5_instance = form.save(commit=False)
            # Link the form instance to the new Submission object
            table5_instance.submission = submission
            # Now save the instance to the database
            table5_instance.save()
            return redirect('table5')
    else:
        form = Table5Form()
    
    rows = Table5Adopter.objects.all().order_by('no', 'id')
    return render(request, 'adopters_features/Table_5_form.html', {'form': form, 'rows': rows})

def table5_edit(request, pk):
    obj = get_object_or_404(Table5Adopter, pk=pk)
    if request.method == 'POST':
        form = Table5Form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('table5')
    else:
        form = Table5Form(instance=obj)
    return render(request, 'adopters_features/Table_5_edit_form.html', {'form': form})

def table5_delete(request, pk):
    return handle_delete(request, pk, Table5Adopter, 'table5')

def export_table5_excel(request):
    qs = Table5Adopter.objects.all().order_by('no', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 5 - Adopters"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table5_adopters.xlsx')

def table5_details(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    form_data = get_object_or_404(Table5Adopter, submission=submission)
    context = {
        'submission': submission,
        'form_data': form_data,
    }
    return render(request, 'adopters_features/Table_5_details.html', context)

# ---------- Table 6 ----------
def table6_view(request):
    if request.method == 'POST':
        form = Table6Form(request.POST, request.FILES)
        if form.is_valid():
            submission = Submission.objects.create(submitter=request.user)
            table6_instance = form.save(commit=False)
            table6_instance.submission = submission
            table6_instance.save()
            return redirect('table6')
    else:
        form = Table6Form()
    
    rows = Table6IEC.objects.all().order_by('no', 'id')
    return render(request, 'adopters_features/Table_6_form.html', {'form': form, 'rows': rows})

def table6_edit(request, pk):
    obj = get_object_or_404(Table6IEC, pk=pk)
    if request.method == 'POST':
        form = Table6Form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('table6')
    else:
        form = Table6Form(instance=obj)
    return render(request, 'adopters_features/Table_6_edit_form.html', {'form': form})

def table6_delete(request, pk):
    return handle_delete(request, pk, Table6IEC, 'table6')

def export_table6_excel(request):
    qs = Table6IEC.objects.all().order_by('no', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 6 - IEC"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table6_iec.xlsx')

def table6_details(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    form_data = get_object_or_404(Table6IEC, submission=submission)
    context = {
        'submission': submission,
        'form_data': form_data,
    }
    return render(request, 'adopters_features/Table_6_details.html', context)

# ---------- Table 7a ----------
def table7a_view(request):
    if request.method == 'POST':
        form = Table7aForm(request.POST, request.FILES)
        if form.is_valid():
            submission = Submission.objects.create(submitter=request.user)
            table7a_instance = form.save(commit=False)
            table7a_instance.submission = submission
            table7a_instance.save()
            return redirect('table7a')
    else:
        form = Table7aForm()
    
    rows = Table7aBudgetGAA.objects.all().order_by('department', 'id')
    return render(request, 'adopters_features/Table_7a_form.html', {'form': form, 'rows': rows})

def table7a_edit(request, pk):
    obj = get_object_or_404(Table7aBudgetGAA, pk=pk)
    if request.method == 'POST':
        form = Table7aForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('table7a')
    else:
        form = Table7aForm(instance=obj)
    return render(request, 'adopters_features/Table_7a_edit_form.html', {'form': form})

def table7a_delete(request, pk):
    return handle_delete(request, pk, Table7aBudgetGAA, 'table7a')

def export_table7a_excel(request):
    qs = Table7aBudgetGAA.objects.all().order_by('department', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 7a - GAA"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table7a_budget_gaa.xlsx')

def table7a_details(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    form_data = get_object_or_404(Table7aBudgetGAA, submission=submission)
    context = {
        'submission': submission,
        'form_data': form_data,
    }
    return render(request, 'adopters_features/Table_7a_details.html', context)

# ---------- Table 7b ----------
def table7b_view(request):
    if request.method == 'POST':
        form = Table7bForm(request.POST, request.FILES)
        if form.is_valid():
            submission = Submission.objects.create(submitter=request.user)
            table7b_instance = form.save(commit=False)
            table7b_instance.submission = submission
            table7b_instance.save()
            return redirect('table7b')
    else:
        form = Table7bForm()
    
    rows = Table7bBudgetIncome.objects.all().order_by('department', 'id')
    return render(request, 'adopters_features/Table_7b_form.html', {'form': form, 'rows': rows})

def table7b_edit(request, pk):
    obj = get_object_or_404(Table7bBudgetIncome, pk=pk)
    if request.method == 'POST':
        form = Table7bForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('table7b')
    else:
        form = Table7bForm(instance=obj)
    return render(request, 'adopters_features/Table_7b_edit_form.html', {'form': form})

def table7b_delete(request, pk):
    return handle_delete(request, pk, Table7bBudgetIncome, 'table7b')

def export_table7b_excel(request):
    qs = Table7bBudgetIncome.objects.all().order_by('department', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 7b - Income"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table7b_budget_income.xlsx')

def table7b_details(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    form_data = get_object_or_404(Table7bBudgetIncome, submission=submission)
    context = {
        'submission': submission,
        'form_data': form_data,
    }
    return render(request, 'adopters_features/Table_7b_details.html', context)

# ---------- Export ALL ----------
def export_all_excel(request):
    wb = Workbook()
    ws5 = wb.active; ws5.title = "Table 5 - Adopters"
    queryset_to_sheet(ws5, Table5Adopter.objects.all().order_by('no', 'id'))
    ws6 = wb.create_sheet(title="Table 6 - IEC")
    queryset_to_sheet(ws6, Table6IEC.objects.all().order_by('no', 'id'))
    ws7a = wb.create_sheet(title="Table 7a - GAA")
    queryset_to_sheet(ws7a, Table7aBudgetGAA.objects.all().order_by('department', 'id'))
    ws7b = wb.create_sheet(title="Table 7b - Income")
    queryset_to_sheet(ws7b, Table7bBudgetIncome.objects.all().order_by('department', 'id'))
    return wb_response(wb, 'all_tables.xlsx')

# ---------- View Submission Details (CENTRALIZED) ----------
def view_submission_details(request, submission_id):
    """
    Kukunin ang isang submission at ang mga kaugnay nitong datos mula sa iba't ibang tables.
    Gagamitin ang ID ng submission para makita ang kumpletong detalye.
    """
    submission = get_object_or_404(Submission, id=submission_id)
    
    data = None
    template_name = None

    try:
        data = submission.table5_data
        template_name = 'adopters_features/table5_details.html'
    except Table5Adopter.DoesNotExist:
        try:
            data = submission.table6_data
            template_name = 'adopters_features/table6_details.html'
        except Table6IEC.DoesNotExist:
            try:
                data = submission.table7a_data
                template_name = 'adopters_features/table7a_details.html'
            except Table7aBudgetGAA.DoesNotExist:
                try:
                    data = submission.table7b_data
                    template_name = 'adopters_features/table7b_details.html'
                except Table7bBudgetIncome.DoesNotExist:
                    return render(request, 'adopters_features/no_data_found.html', {'submission': submission})

    context = {
        'submission': submission,
        'data': data,
    }
    
    return render(request, template_name, context)
