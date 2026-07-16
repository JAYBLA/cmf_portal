from django.db import models
from num2words import num2words
from invoices.models import Invoice

# =========================================
# RECEIPT
# =========================================


class Receipt(models.Model):

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("tcb bank deposit", "TCB BANK DEPOSIT"),
        ("nmb bank deposit", "NMB BANK DEPOSIT"),
        ("tcb bank cheque", "TCB BANK CHEQUE"),
        ("nmb bank cheque", "NMB BANK CHEQUE"),        
    )

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="receipts",
    )

    receipt_date = models.DateField()

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="cash",
    )

    payment_proof = models.FileField(
        upload_to="receipts/payment_proofs/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Payment Proof",
        help_text="Upload bank deposit slip, mobile money receipt, cheque scan or payment screenshot.",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-id",
        ]

    def save(self, *args, **kwargs):

        # =====================================
        # AUTO RECEIPT NUMBER
        # =====================================

        if not self.receipt_number:

            last_receipt = Receipt.objects.order_by("-id").first()

            if last_receipt:

                try:

                    last_id = int(last_receipt.receipt_number.split("-")[-1])

                    next_id = last_id + 1

                except (
                    ValueError,
                    AttributeError,
                ):

                    next_id = last_receipt.id + 1

            else:

                next_id = 1

            self.receipt_number = f"RCT-{next_id:05d}"

        super().save(
            *args,
            **kwargs,
        )

    @property
    def customer(self):

        return self.invoice.customer

    @property
    def amount_in_words(self):

        amount = int(self.amount)

        words = num2words(
            amount,
            lang="en",
        ).title()

        return f"{words} Only."

    def __str__(self):

        return self.receipt_number
