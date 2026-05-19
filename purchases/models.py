from django.db import models
from products.models import Product
from suppliers.models import Supplier
from django.utils import timezone

# =========================================
# PURCHASE
# =========================================
class Purchase(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchases"
    )

    purchase_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    supplier_invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    purchase_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-id"]


    def save(self, *args, **kwargs):

        # GENERATE PURCHASE NUMBER

        if not self.purchase_number:

            year = timezone.now().year

            last_purchase = Purchase.objects.filter(
                purchase_number__startswith=f"PUR-{year}"
            ).order_by("-id").first()

            if last_purchase:

                last_number = int(
                    last_purchase.purchase_number.split("-")[-1]
                )

                new_number = last_number + 1

            else:

                new_number = 1

            self.purchase_number = (
                f"PUR-{year}-{new_number:05d}"
            )

        super().save(*args, **kwargs)


    def __str__(self):

        return self.purchase_number
    
class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_items"
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:

        ordering = ["id"]

    @property
    def subtotal(self):

        return self.quantity * self.unit_cost

    def __str__(self):

        return f"{self.product.product_name}"
