from django.contrib import admin

from .models import Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_editable = ("is_active",)
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "expense_number",
        "expense_date",
        "category",
        "payee",
        "amount",
        "payment_method",
    )
    list_filter = ("category", "payment_method", "expense_date")
    search_fields = (
        "expense_number",
        "payee__customer_name",
        "description",
        "reference_number",
    )
