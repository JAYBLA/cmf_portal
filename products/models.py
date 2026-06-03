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
    
    # =========================================
    # STOCK MANAGEMENT
    # =========================================

    current_stock = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0

    )

    minimum_stock = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0

    )

    average_cost = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0

    )

    stock_value = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )
    # =========================================
    # STOCK STATUS
    # =========================================

    @property
    def stock_status(self):

        if self.current_stock <= 0:

            return "out"

        elif self.current_stock <= self.minimum_stock:

            return "low"

        return "in"



    # =========================================
    # UPDATE STOCK VALUE
    # =========================================

    def update_stock_value(self):

        self.stock_value = (

            self.current_stock *

            self.average_cost

        )

        self.save(
            update_fields=[
                "stock_value"
            ]
        )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return f"{self.product_name} ({self.sku_code})"
    
    # =========================================
    # UPDATE STOCK
    # =========================================

    def update_stock(

        self,

        quantity,

        movement_type="in",

        unit_cost=0,

        reference=None,

        notes=None

    ):

        # =====================================
        # STOCK IN
        # =====================================

        if movement_type == "in":

            self.current_stock += quantity

        # =====================================
        # STOCK OUT
        # =====================================

        elif movement_type == "out":

            self.current_stock -= quantity

        # =====================================
        # ADJUSTMENT
        # =====================================

        else:

            self.current_stock += quantity

        # =====================================
        # UPDATE STOCK VALUE
        # =====================================

        self.stock_value = (

            self.current_stock *

            self.average_cost

        )

        self.save()

        # =====================================
        # CREATE MOVEMENT
        # =====================================

        StockMovement.objects.create(

            product=self,

            movement_type=movement_type,

            quantity=quantity,

            balance_after=self.current_stock,

            unit_cost=unit_cost,

            total_cost=(

                quantity *

                unit_cost

            ),

            reference=reference,

            notes=notes

        )
# =========================================
# STOCK MOVEMENT
# =========================================

class StockMovement(models.Model):

    MOVEMENT_TYPES = (

        ("in", "Stock In"),

        ("out", "Stock Out"),

        ("adjustment", "Adjustment"),

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        related_name="stock_movements"

    )

    movement_type = models.CharField(

        max_length=20,

        choices=MOVEMENT_TYPES

    )

    quantity = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    balance_after = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0

    )

    unit_cost = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=0

    )

    total_cost = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    reference = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )

    notes = models.TextField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-id"]

    def __str__(self):

        return (

            f"{self.product} - "
            f"{self.get_movement_type_display()}"

        )