from django.contrib import admin

from .models import Lending, LendingItem


class LendingItemInline(admin.TabularInline):
    model = LendingItem
    extra = 0


@admin.register(Lending)
class LendingAdmin(admin.ModelAdmin):
    list_display = ("lending_number", "customer", "lending_date", "due_date", "return_status")
    list_filter = ("return_status", "lending_date", "due_date")
    search_fields = ("customer__customer_name", "customer__company_name", "purpose")
    inlines = (LendingItemInline,)


@admin.register(LendingItem)
class LendingItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "asset_tag", "lending", "quantity", "returned_quantity")
    search_fields = ("item_name", "asset_tag", "lending__customer__customer_name")
