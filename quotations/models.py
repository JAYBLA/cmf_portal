from django.db import models

from customers.models import Customer


class Quotation(models.Model):

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quotations"
    )

    quote_date = models.DateField()

    due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title
    
    @property
    def total_amount(self):
        return sum(
            item.total
            for item in self.items.all()
        )


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_name = models.CharField(
        max_length=255
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.item_name

    @property
    def total(self):
        return self.quantity * self.unit_price