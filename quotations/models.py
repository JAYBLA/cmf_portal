from django.db import models

from customers.models import *

from products.models import *

# =========================================
# QUOTATION
# =========================================

class Quotation(models.Model):

    STATUS = (

        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
        ("converted", "Converted"),

    )

    quotation_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="quotations"
    )

    quotation_date = models.DateField()

    valid_until = models.DateField()

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

    class Meta:

        ordering = ["-id"]

    def __str__(self):

        return self.quotation_number

    # =====================================
    # AUTO GENERATE QUOTATION NUMBER
    # =====================================

    def save(self, *args, **kwargs):

        if not self.quotation_number:

            last_quotation = (
                Quotation.objects
                .order_by("-id")
                .first()
            )

            if last_quotation:

                try:

                    last_number = int(
                        last_quotation.quotation_number
                        .replace("QTN-", "")
                    )

                except (ValueError, AttributeError):

                    last_number = 0

                next_number = (
                    last_number + 1
                )

            else:

                next_number = 1

            self.quotation_number = (
                f"QTN-{next_number:05d}"
            )

        super().save(*args, **kwargs)
    
# =========================================
# QUOTATION ITEM
# =========================================

class QuotationItem(models.Model):

    quotation = models.ForeignKey(

        Quotation,

        on_delete=models.CASCADE,

        related_name="items"

    )

    # OPTIONAL PRODUCT

    product = models.ForeignKey(

        Product,

        on_delete=models.SET_NULL,

        blank=True,

        null=True,

        related_name="quotation_items"

    )

    # DESCRIPTION ALWAYS REQUIRED

    description = models.CharField(

        max_length=255

    )

    quantity = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=1

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

    def save(

        self,

        *args,

        **kwargs

    ):

        self.subtotal = (

            self.quantity *

            self.unit_price

        )

        super().save(

            *args,

            **kwargs

        )

    def __str__(self):

        return self.description