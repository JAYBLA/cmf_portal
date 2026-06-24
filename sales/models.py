from django.db import models
from customers.models import *
from products.models import *
from purchases.models import *
from decimal import Decimal

class Sale(models.Model):

    SALE_STATUS = (
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales",
    )

    sale_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
    )

    sale_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True,
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    amount_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("partial", "Partial"),
            ("paid", "Paid"),
        ),
        default="pending",
    )

    status = models.CharField(
        max_length=20,
        choices=SALE_STATUS,
        default="draft",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    
class SalePayment(models.Model):

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("mobile", "Mobile Money"),
        ("cheque", "Cheque"),
    )

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

class SalesProductPricing(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="sales_pricing"
    )

    purchase_pricing = models.ForeignKey(
        PurchaseProductPricing,
        on_delete=models.PROTECT,
        related_name="sales_pricing_history"
    )

    landed_unit_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    markup_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100
    )

    selling_price = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    effective_date = models.DateField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):

        self.selling_price = (
            self.landed_unit_cost *
            (
                Decimal("1.00") +
                (self.markup_percentage / Decimal("100"))
            )
        )

        super().save(*args, **kwargs)