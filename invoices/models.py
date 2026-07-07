from decimal import Decimal

from django.db import models
from django.db.models import Sum

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
    INVOICE_TYPES = (
        ("invoice", "Invoice"),
        ("proforma", "Proforma"),
    )

    invoice_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="invoices"
    )
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES, default="invoice")
    invoice_date = models.DateField()

    due_date = models.DateField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS, default="draft")

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-id"]

    def save(self, *args, **kwargs):

        # =====================================
        # AUTO NUMBER
        # =====================================

        if not self.invoice_number:

            last_invoice = Invoice.objects.order_by("-id").first()

            if last_invoice:

                last_id = int(last_invoice.invoice_number.split("-")[-1])

                next_id = last_id + 1

            else:

                next_id = 1

            self.invoice_number = f"INV-{next_id:05d}"

        super().save(*args, **kwargs)
    def update_payment_status(self):

        amount_paid = (
            self.receipts.aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        self.amount_paid = amount_paid

        self.balance = (
            self.total_amount
            - amount_paid
        )


        # =====================================
        # CONVERT PROFORMA TO INVOICE
        # =====================================

        if (
            amount_paid > Decimal("0.00")
            and self.invoice_type == "proforma"
        ):

            self.invoice_type = "invoice"


        # =====================================
        # UPDATE PAYMENT STATUS
        # =====================================

        if (
            self.total_amount > 0
            and self.balance <= 0
        ):

            self.status = "paid"

        elif amount_paid > 0:

            self.status = "partial"

        elif self.total_amount > 0:

            self.status = "unpaid"

        else:

            self.status = "draft"


        # =====================================
        # SAVE INVOICE
        # =====================================

        self.save(
            update_fields=[
                "amount_paid",
                "balance",
                "status",
                "invoice_type",
            ]
        )

    def __str__(self):

        return self.invoice_number


# =========================================
# INVOICE ITEM
# =========================================


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="invoice_items",
        blank=True,
        null=True,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    unit_price = models.DecimalField(max_digits=14, decimal_places=2)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def save(self, *args, **kwargs):

        self.subtotal = self.quantity * self.unit_price

        super().save(*args, **kwargs)
