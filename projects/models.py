from django.db import models
from django.db.models import Sum
from decimal import Decimal
from datetime import date


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        ACTIVE = "active", "Active"
        ON_HOLD = "on_hold", "On hold"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    project_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.project_name

    @property
    def total_expenses(self):
        return self.expenses.aggregate(total=Sum("amount"))["total"] or 0

    @property
    def profit(self):
        return (self.budget or 0) - self.total_expenses


class ProjectExpense(models.Model):
    class ExpenseType(models.TextChoices):
        MATERIAL = "material", "Material"
        LABOUR = "labour", "Labour"
        TRANSPORT = "transport", "Transport"
        EQUIPMENT = "equipment", "Equipment"
        OTHER = "other", "Other"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses")
    expense_type = models.CharField(max_length=20, choices=ExpenseType.choices, default=ExpenseType.MATERIAL)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    expense_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-expense_date", "-id")

    def __str__(self):
        return f"{self.project} - {self.description}"

    def save(self, *args, **kwargs):
        if not self.expense_type:
            self.expense_type = self.ExpenseType.MATERIAL
        if not self.expense_date:
            self.expense_date = date.today()
        self.amount = (self.quantity or Decimal("0")) * (self.unit_price or Decimal("0"))
        super().save(*args, **kwargs)
