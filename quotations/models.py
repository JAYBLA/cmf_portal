from django.db import models

from customers.models import Customer
from decimal import Decimal
from django.db.models import Sum


class Quotation(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, null=True)

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="quotations"
    )

    quote_date = models.DateField()

    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    @property
    def total_amount(self):
        return sum(item.total for item in self.items.all())

    @property
    def quoted_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def delivered_quantity(self):
        return sum(item.delivered_quantity for item in self.items.all())

    @property
    def remaining_quantity(self):
        return sum(item.remaining_quantity for item in self.items.all())

    @property
    def delivery_percentage(self):
        if self.quoted_quantity == 0:
            return 0

        return round((self.delivered_quantity / self.quoted_quantity) * 100, 2)

    @property
    def delivery_status(self):
        if self.delivered_quantity == 0:
            return "Pending"

        if self.remaining_quantity == 0:
            return "Completed"

        return "Partial"


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name="items"
    )

    item_name = models.CharField(max_length=255)

    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.item_name

    @property
    def total(self):
        return self.quantity * self.unit_price

    @property
    def delivered_quantity(self):
        """
        Total quantity delivered across all delivery notes
        for this quotation item.
        """
        return self.delivery_items.aggregate(total=Sum("quantity"))["total"] or Decimal(
            "0"
        )

    @property
    def remaining_quantity(self):
        """
        Quantity still remaining to be delivered.
        """
        remaining = self.quantity - self.delivered_quantity
        return max(remaining, Decimal("0"))

    @property
    def is_fully_delivered(self):
        """
        Returns True if the quotation item has been completely delivered.
        """
        return self.remaining_quantity == Decimal("0")

    @property
    def delivery_percentage(self):
        """
        Percentage of this quotation item that has been delivered.
        """
        if self.quantity == 0:
            return 0

        return round((self.delivered_quantity / self.quantity) * 100, 2)
