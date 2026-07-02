from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from quotations.models import Quotation, QuotationItem


class DeliveryNote(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("partial", "Partially Delivered"),
        ("completed", "Completed"),
    )

    delivery_number = models.CharField(max_length=30, unique=True, editable=False)

    quotation = models.ForeignKey(
        Quotation, on_delete=models.PROTECT, related_name="delivery_notes"
    )

    delivery_date = models.DateField()

    delivery_address = models.TextField(blank=True)

    receiver_name = models.CharField(max_length=255, blank=True)

    receiver_phone = models.CharField(max_length=50, blank=True)

    driver_name = models.CharField(max_length=255, blank=True)

    vehicle_number = models.CharField(max_length=100, blank=True)

    notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.delivery_number

    @property
    def customer(self):
        return self.quotation.customer

    @property
    def quoted_quantity(self):
        return sum(item.quantity for item in self.quotation.items.all())

    @property
    def delivered_quantity(self):
        return self.items.aggregate(total=Sum("quantity"))["total"] or Decimal("0")

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    def save(self, *args, **kwargs):

        if not self.delivery_number:

            today = timezone.now().strftime("%Y%m%d")

            last = (
                DeliveryNote.objects.filter(delivery_number__startswith=f"DN-{today}")
                .order_by("-id")
                .first()
            )

            if last:
                number = int(last.delivery_number.split("-")[-1]) + 1
            else:
                number = 1

            self.delivery_number = f"DN-{today}-{number:04d}"

        super().save(*args, **kwargs)


class DeliveryNoteItem(models.Model):

    delivery_note = models.ForeignKey(
        DeliveryNote, on_delete=models.CASCADE, related_name="items"
    )

    quotation_item = models.ForeignKey(
        QuotationItem, on_delete=models.PROTECT, related_name="delivery_items"
    )

    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.quotation_item.item_name

    @property
    def item_name(self):
        return self.quotation_item.item_name

    @property
    def quoted_quantity(self):
        return self.quotation_item.quantity

    @property
    def unit_price(self):
        return self.quotation_item.unit_price

    @property
    def total_price(self):
        return self.quantity * self.unit_price
