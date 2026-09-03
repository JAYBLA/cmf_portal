from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from customers.models import Customer


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Expense categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer / Deposit"),
        ("mobile", "Mobile Money"),
        ("cheque", "Cheque"),
    )

    expense_number = models.CharField(max_length=30, unique=True, blank=True)
    expense_date = models.DateField(default=timezone.localdate)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name="expenses",
    )
    payee = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="expenses",
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="cash",
    )
    reference_number = models.CharField(max_length=100, blank=True)
    supporting_document = models.FileField(
        upload_to="expenses/documents/%Y/%m/",
        blank=True,
        null=True,
        help_text="Upload a receipt, invoice, payment slip, or other supporting document.",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expense_date", "-id"]

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and not self.expense_number:
            self.expense_number = f"CMFE00{self.pk}"
            type(self).objects.filter(pk=self.pk).update(
                expense_number=self.expense_number,
            )

    def __str__(self):
        return f"{self.expense_number} - {self.description}"
