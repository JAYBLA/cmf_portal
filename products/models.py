from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.name


class ProductUnit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.abbreviation or self.name


class Product(models.Model):

    PRODUCT_TYPE_CHOICES = (
        ("stock", "Stock Item"),
        ("service", "Service"),
        ("consumable", "Consumable"),
        ("asset", "Asset"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    product_name = models.CharField(max_length=255)

    short_description = models.TextField(blank=True, null=True)

    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products"
    )

    sku_code = models.CharField(max_length=100, unique=True)

    product_unit = models.ForeignKey(
        ProductUnit, on_delete=models.PROTECT, related_name="products"
    )

    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return f"{self.product_name} ({self.sku_code})"
