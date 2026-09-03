from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from customers.models import Customer


class Lending(models.Model):
    class ReturnStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        PARTIAL = "partial", "Partially returned"
        RETURNED = "returned", "Returned"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="lendings",
    )
    lending_date = models.DateField(default=date.today)
    due_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    return_status = models.CharField(
        max_length=20,
        choices=ReturnStatus.choices,
        default=ReturnStatus.ACTIVE,
        editable=False,
    )
    purpose = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-lending_date", "-id")

    def __str__(self):
        return f"{self.lending_number} - {self.customer}"

    @property
    def lending_number(self):
        return f"CMFL00{self.pk}" if self.pk else "CMFL"

    @property
    def total_quantity(self):
        return self.items.aggregate(total=Sum("quantity"))["total"] or 0

    @property
    def returned_quantity(self):
        return self.items.aggregate(total=Sum("returned_quantity"))["total"] or 0

    @property
    def outstanding_quantity(self):
        return max(self.total_quantity - self.returned_quantity, 0)

    @property
    def is_overdue(self):
        return bool(
            self.due_date
            and self.due_date < date.today()
            and self.return_status != self.ReturnStatus.RETURNED
        )

    @property
    def display_status(self):
        return "Overdue" if self.is_overdue else self.get_return_status_display()

    def refresh_return_status(self, save=True):
        total = self.total_quantity
        returned = self.returned_quantity
        if total and returned >= total:
            self.return_status = self.ReturnStatus.RETURNED
            if not self.returned_date:
                self.returned_date = date.today()
        elif returned:
            self.return_status = self.ReturnStatus.PARTIAL
            self.returned_date = None
        else:
            self.return_status = self.ReturnStatus.ACTIVE
            self.returned_date = None
        if save:
            self.save(update_fields=("return_status", "returned_date", "updated_at"))


class LendingItem(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "New"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        POOR = "poor", "Poor"
        DAMAGED = "damaged", "Damaged"

    lending = models.ForeignKey(
        Lending,
        on_delete=models.CASCADE,
        related_name="items",
    )
    item_name = models.CharField(max_length=255)
    asset_tag = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    returned_quantity = models.PositiveIntegerField(default=0)
    condition_out = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD,
    )
    condition_return = models.CharField(
        max_length=20,
        choices=Condition.choices,
        blank=True,
    )
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.item_name

    @property
    def outstanding_quantity(self):
        return max(self.quantity - self.returned_quantity, 0)

    def clean(self):
        if self.returned_quantity > self.quantity:
            raise ValidationError({
                "returned_quantity": "Returned quantity cannot exceed the quantity lent."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
