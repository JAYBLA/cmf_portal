from decimal import Decimal

from django.db import models
from django.utils import timezone

from products.models import Product
from suppliers.models import Supplier
from agents.models import ClearingAgent

# =========================================
# PURCHASE
# =========================================


class Purchase(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    )

    PURCHASE_CATEGORIES = (
        ("international", "International"),
        ("local", "Local"),
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchases",
    )

    purchase_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
    )

    purchase_category = models.CharField(
        max_length=20,
        choices=PURCHASE_CATEGORIES,
        default="international",
    )

    currency = models.CharField(
        max_length=10,
        choices=(
            ("USD", "USD"),
            ("TZS", "TZS"),
        ),
        default="TZS",
    )

    exchange_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
    )

    supplier_invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    purchase_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True,
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

    total_amount_tzs = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    amount_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    @property
    def landed_cost_tzs(self):

        additional_costs = sum(cost.amount_tzs for cost in self.additional_costs.all())

        return self.total_amount_tzs + additional_costs

    @property
    def balance_tzs(self):

        if self.currency == "USD":
            return self.balance * self.exchange_rate

        return self.balance

    def save(self, *args, **kwargs):

        if not self.purchase_number:

            year = timezone.now().year

            last_purchase = (
                Purchase.objects.filter(purchase_number__startswith=f"PUR-{year}")
                .order_by("-id")
                .first()
            )

            next_number = 1

            if last_purchase:
                next_number = int(last_purchase.purchase_number.split("-")[-1]) + 1

            self.purchase_number = f"PUR-{year}-{next_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.purchase_number


# =========================================
# PURCHASE ITEM
# =========================================


class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_items",
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        ordering = ["id"]

    @property
    def subtotal(self):
        return self.quantity * self.unit_cost

    @property
    def subtotal_tzs(self):

        if self.purchase.currency == "USD":
            return self.subtotal * self.purchase.exchange_rate

        return self.subtotal

    @property
    def value_percentage(self):

        purchase_total = sum(item.subtotal_tzs for item in self.purchase.items.all())

        if purchase_total <= 0:
            return Decimal("0")

        return self.subtotal_tzs / purchase_total

    @property
    def allocated_additional_cost(self):

        total_additional_costs = sum(
            cost.amount_tzs for cost in self.purchase.additional_costs.all()
        )

        return total_additional_costs * self.value_percentage

    @property
    def landed_cost_total(self):

        return self.subtotal_tzs + self.allocated_additional_cost

    @property
    def landed_unit_cost(self):

        if self.quantity <= 0:
            return Decimal("0")

        return self.landed_cost_total / self.quantity

    def __str__(self):
        return self.product.product_name


# =========================================
# PURCHASE PAYMENT
# =========================================


class PurchasePayment(models.Model):

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("mobile", "Mobile Money"),
        ("cheque", "Cheque"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    payment_date = models.DateField(default=timezone.now)

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.purchase.purchase_number} - {self.amount}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        self.update_purchase_payment_status()

    def delete(self, *args, **kwargs):

        purchase = self.purchase

        super().delete(*args, **kwargs)

        self.update_purchase_totals(purchase)

    def update_purchase_payment_status(self):

        self.update_purchase_totals(self.purchase)

    @staticmethod
    def update_purchase_totals(purchase):

        total_paid = (
            purchase.payments.aggregate(total=models.Sum("amount"))["total"] or 0
        )

        purchase.amount_paid = total_paid
        purchase.balance = purchase.total_amount - total_paid

        if purchase.total_amount <= 0:
            purchase.payment_status = "pending"

        elif total_paid <= 0:
            purchase.payment_status = "pending"

        elif total_paid < purchase.total_amount:
            purchase.payment_status = "partial"

        else:
            purchase.payment_status = "paid"

        purchase.save()


# =========================================
# PURCHASE ADDITIONAL COST
# =========================================


class PurchaseAdditionalCost(models.Model):

    COST_TYPES = (
        ("shipping_international", "International Shipping"),
        ("shipping_local", "Local Transport"),
        ("tax", "Import Tax"),
        ("clearing", "Clearing Charges"),
        ("port", "Port Charges"),
        ("insurance", "Insurance"),
        ("other", "Other"),
    )

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
    )

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="additional_costs",
    )

    clearing_agent = models.ForeignKey(
        ClearingAgent,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="costs",
    )

    cost_type = models.CharField(
        max_length=50,
        choices=COST_TYPES,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
        choices=(
            ("USD", "USD"),
            ("TZS", "TZS"),
        ),
        default="TZS",
    )

    exchange_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending",
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["id"]

    @property
    def amount_tzs(self):

        if self.currency == "USD":
            return self.amount * self.exchange_rate

        return self.amount

    def __str__(self):
        return self.get_cost_type_display()


# =========================================
# ADDITIONAL COST DOCUMENT
# =========================================


class AdditionalCostDocument(models.Model):

    additional_cost = models.ForeignKey(
        PurchaseAdditionalCost,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to="additional_costs/documents/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PurchaseProductPricing(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    purchase_item = models.OneToOneField(PurchaseItem, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    purchase_value_tzs = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    allocated_cost_tzs = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    landed_cost_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    landed_unit_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
