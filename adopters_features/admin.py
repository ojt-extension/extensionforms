from django.contrib import admin
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

@admin.register(Table5Adopter)
class Table5Admin(admin.ModelAdmin):
    list_display = ("adopter_name", "lead_unit", "adopter_category", "monthly_income_before", "monthly_income_after")
    search_fields = ("adopter_name", "lead_unit", "adopter_category", "projects_involved")
    list_filter = ("adopter_sex", "adopter_category", "lead_unit")

@admin.register(Table6IEC)
class Table6Admin(admin.ModelAdmin):
    list_display = ("title", "format", "lead_unit", "total_recipients", "project_no")
    search_fields = ("title", "lead_unit", "project_no", "sdg", "thematic_area")
    list_filter = ("format", "lead_unit")

@admin.register(Table7aBudgetGAA)
class Table7aAdmin(admin.ModelAdmin):
    list_display = ("department", "allocated_budget", "amount_utilized")
    search_fields = ("department", "curricular_offering")

@admin.register(Table7bBudgetIncome)
class Table7bAdmin(admin.ModelAdmin):
    list_display = ("department", "allocated_budget", "amount_utilized")
    search_fields = ("department", "curricular_offering")
