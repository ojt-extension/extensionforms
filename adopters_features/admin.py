from django.contrib import admin
from .models import Table5Adopter, Table6IEC, Table7aBudgetGAA, Table7bBudgetIncome

@admin.register(Table5Adopter)
class Table5Admin(admin.ModelAdmin):
    list_display = ('id', 'no', 'adopter_name', 'department_unit', 'contact_person', 'contact_number_email', 'date_started')
    list_filter = ('department_unit', 'contact_person', 'date_started')
    search_fields = ('adopter_name', 'department_unit')

@admin.register(Table6IEC)
class Table6Admin(admin.ModelAdmin):
    list_display = ('id', 'no', 'title', 'department_unit', 'contact_person', 'contact_number_email')
    list_filter = ('department_unit',)
    search_fields = ('title', 'department_unit')

@admin.register(Table7aBudgetGAA)
class Table7aAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'total_budget_allocated', 'allocated_budget', 'amount_utilized', 'remarks')
    list_filter = ('department',)
    search_fields = ('department',)

@admin.register(Table7bBudgetIncome)
class Table7bAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'total_budget_allocated', 'allocated_budget', 'amount_utilized', 'remarks')
    list_filter = ('department',)
    search_fields = ('department',)
