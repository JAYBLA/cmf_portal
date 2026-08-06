from decimal import Decimal

from django.db import models
from django.utils import timezone


class Voucher(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    voucher_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
    )

    voucher_date = models.DateField(
        default=timezone.now,
    )

    payee_name = models.CharField(
        max_length=255,
    )

    payee_phone = models.CharField(
        max_length=30,
        blank=True,
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

    approved_by = models.CharField(
        max_length=255,
    )

    received_by = models.CharField(
        max_length=255,
    )

    notes = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.voucher_number = f"CMFV00{self.pk}"
            type(self).objects.filter(pk=self.pk).update(
                voucher_number=self.voucher_number,
            )

    def __str__(self):
        return self.voucher_number
    
class VoucherItem(models.Model):

    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        related_name="items",
    )

    description = models.CharField(
        max_length=255,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    class Meta:
        ordering = ["id"]

    @property
    def subtotal(self):
        return self.amount

    def __str__(self):
        return self.description
