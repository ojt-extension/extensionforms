from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import Table5Form, Table6Form, Table7aForm, Table7bForm
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome
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

# ---------- Generic Helpers ----------
def handle_create(request, form_class, redirect_name):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(redirect_name)
    else:
        form = form_class()
    return form

def handle_edit(request, pk, model_class, form_class, redirect_name):
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(redirect_name)
    else:
        form = form_class(instance=obj)
    return form

def handle_delete(request, pk, model_class, redirect_name):
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect(redirect_name)

# ---------- Table 5 ----------
def table5_view(request):
    form = handle_create(request, Table5Form, 'table5')
    rows = Table5Adopter.objects.all().order_by('no', 'id')
    return render(request, 'adopters_features/Table_5_form.html', {'form': form, 'rows': rows})

def table5_edit(request, pk):
    return handle_edit(request, pk, Table5Adopter, Table5Form, 'table5')

def table5_delete(request, pk):
    return handle_delete(request, pk, Table5Adopter, 'table5')

def export_table5_excel(request):
    qs = Table5Adopter.objects.all().order_by('no', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 5 - Adopters"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table5_adopters.xlsx')

# ---------- Table 6 ----------
def table6_view(request):
    form = handle_create(request, Table6Form, 'table6')
    rows = Table6IEC.objects.all().order_by('no', 'id')
    return render(request, 'adopters_features/Table_6_form.html', {'form': form, 'rows': rows})

def table6_edit(request, pk):
    return handle_edit(request, pk, Table6IEC, Table6Form, 'table6')

def table6_delete(request, pk):
    return handle_delete(request, pk, Table6IEC, 'table6')

def export_table6_excel(request):
    qs = Table6IEC.objects.all().order_by('no', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 6 - IEC"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table6_iec.xlsx')

# ---------- Table 7a ----------
def table7a_view(request):
    form = handle_create(request, Table7aForm, 'table7a')
    rows = Table7aBudgetGAA.objects.all().order_by('department', 'id')
    return render(request, 'adopters_features/Table_7a_form.html', {'form': form, 'rows': rows})

def table7a_edit(request, pk):
    return handle_edit(request, pk, Table7aBudgetGAA, Table7aForm, 'table7a')

def table7a_delete(request, pk):
    return handle_delete(request, pk, Table7aBudgetGAA, 'table7a')

def export_table7a_excel(request):
    qs = Table7aBudgetGAA.objects.all().order_by('department', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 7a - GAA"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table7a_budget_gaa.xlsx')

# ---------- Table 7b ----------
def table7b_view(request):
    form = handle_create(request, Table7bForm, 'table7b')
    rows = Table7bBudgetIncome.objects.all().order_by('department', 'id')
    return render(request, 'adopters_features/Table_7b_form.html', {'form': form, 'rows': rows})

def table7b_edit(request, pk):
    return handle_edit(request, pk, Table7bBudgetIncome, Table7bForm, 'table7b')

def table7b_delete(request, pk):
    return handle_delete(request, pk, Table7bBudgetIncome, 'table7b')

def export_table7b_excel(request):
    qs = Table7bBudgetIncome.objects.all().order_by('department', 'id')
    wb = Workbook(); ws = wb.active; ws.title = "Table 7b - Income"
    queryset_to_sheet(ws, qs)
    return wb_response(wb, 'table7b_budget_income.xlsx')

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
