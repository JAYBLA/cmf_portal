from decimal import Decimal
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ProductCategory(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProductUnit(models.Model):

    name = models.CharField(max_length=50, unique=True)

    abbreviation = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.abbreviation or self.name


from django.db import models


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

    product_name = models.CharField(
        max_length=255,
    )

    short_description = models.TextField(
        blank=True,
        null=True,
    )

    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
    )

    sku_code = models.CharField(
        max_length=100,
        unique=True,
    )

    product_unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.PROTECT,
        related_name="products",
    )

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default="stock",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active",
    )
    is_tangible = models.BooleanField(
        default=True,
    )

    # =====================================
    # INVENTORY
    # =====================================

    # Cached stock balance.
    # Updated ONLY through the Stock Movement Service.
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["product_name"]

    @property
    def stock_status(self):
        """
        Returns:
            out  -> No stock
            low  -> Stock is at or below minimum
            in   -> Sufficient stock
        """

        if self.current_stock <= 0:
            return "out"

        if self.current_stock <= self.minimum_stock:
            return "low"

        return "in"

    @property
    def stock_percentage(self):
        """
        Returns the stock level as a percentage
        relative to the minimum stock level.
        """

        total = self.current_stock + self.minimum_stock

        if total <= 0:
            return 0

        percentage = (self.current_stock / total) * 100

        return min(round(float(percentage)), 100)

    @property
    def is_in_stock(self):
        return self.current_stock > 0

    @property
    def is_low_stock(self):
        return self.current_stock > 0 and self.current_stock <= self.minimum_stock

    @property
    def is_out_of_stock(self):
        return self.current_stock <= 0

    def __str__(self):
        return f"{self.product_name} ({self.sku_code})"


class StockMovement(models.Model):

    MOVEMENT_TYPES = (
        ("purchase", "Purchase"),
        ("sale", "Sale"),
        ("lending", "Lending"),
        ("return", "Return"),
        ("adjustment", "Adjustment"),
        ("production", "Production"),
        ("damage", "Damage"),
        ("transfer", "Transfer"),
    )

    DIRECTION = (
        ("in", "Stock In"),
        ("out", "Stock Out"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_movements",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
    )

    direction = models.CharField(
        max_length=10,
        choices=DIRECTION,
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    balance_after = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    # Generic reference
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    reference = GenericForeignKey(
        "content_type",
        "object_id",
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
