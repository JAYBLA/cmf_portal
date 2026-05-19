from django.contrib import admin
from .models import ProductCategory, ProductUnit

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(ProductUnit)