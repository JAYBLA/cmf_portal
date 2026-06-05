from django.db import models

from customers.models import *
from products.models import *
from quotations.models import *


# =========================================
# INVOICE
# =========================================

class Invoice(models.Model):

    STATUS = (

        ("draft", "Draft"),

        ("unpaid", "Unpaid"),

        ("partial", "Partial"),

        ("paid", "Paid"),

        ("cancelled", "Cancelled"),

    )

    invoice_number = models.CharField(

        max_length=30,

        unique=True,

        blank=True

    )

    customer = models.ForeignKey(

        Customer,

        on_delete=models.PROTECT,

        related_name="invoices"

    )

    quotation = models.OneToOneField(

        Quotation,

        on_delete=models.SET_NULL,

        blank=True,

        null=True,

        related_name="invoice"

    )

    invoice_date = models.DateField()

    due_date = models.DateField(

        blank=True,

        null=True

    )

    subtotal = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    discount_amount = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    total_amount = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    amount_paid = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    balance = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="draft"

    )

    notes = models.TextField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["-id"]

    def save(self, *args, **kwargs):

        # =====================================
        # AUTO NUMBER
        # =====================================

        if not self.invoice_number:

            last_invoice = Invoice.objects.order_by(
                "-id"
            ).first()

            if last_invoice:

                last_id = int(
                    last_invoice.invoice_number.split("-")[-1]
                )

                next_id = last_id + 1

            else:

                next_id = 1

            self.invoice_number = (
                f"INV-{next_id:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.invoice_number
    
# =========================================
# INVOICE ITEM
# =========================================

class InvoiceItem(models.Model):

    invoice = models.ForeignKey(

        Invoice,

        on_delete=models.CASCADE,

        related_name="items"

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.PROTECT,

        related_name="invoice_items"

    )

    quantity = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    unit_price = models.DecimalField(

        max_digits=14,

        decimal_places=2

    )

    subtotal = models.DecimalField(

        max_digits=14,

        decimal_places=2,

        default=0

    )

    class Meta:

        ordering = ["id"]

    def save(self, *args, **kwargs):

        self.subtotal = (

            self.quantity *

            self.unit_price

        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product}"
        )