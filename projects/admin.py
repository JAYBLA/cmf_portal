from django.contrib import admin

from .models import Project, ProjectExpense


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name", "client_name", "status", "start_date", "end_date", "budget")
    list_filter = ("status",)
    search_fields = ("project_name", "client_name")


@admin.register(ProjectExpense)
class ProjectExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "project", "expense_type", "quantity", "unit_price", "amount", "expense_date")
    list_filter = ("expense_type", "expense_date")
    search_fields = ("description", "project__project_name")
