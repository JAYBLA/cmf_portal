from django.db import models
from products.models import Product
from suppliers.models import Supplier
from django.utils import timezone
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
        Supplier, on_delete=models.PROTECT, related_name="purchases"
    )

    purchase_number = models.CharField(max_length=50, unique=True, blank=True)
    purchase_category = models.CharField(
        max_length=100, blank=True, null=True, choices=PURCHASE_CATEGORIES
    )
    currency = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=(
            ("USD", "USD"),
            ("TZS", "TZS"),
        ),
    )
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=2)
    international_shipping_cost = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    local_shipping_cost = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    supplier_invoice_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount_tzs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ["-id"]
        
    # =========================================
    # LANDED COST TZS
    # =========================================

    @property
    def landed_cost_tzs(self):

        additional_costs = Decimal("0.00")

        for cost in self.additional_costs.all():

            additional_costs += cost.amount_tzs

        return (

            self.total_amount_tzs +

            additional_costs

        )

    # =========================================
    # BALANCE TZS EQUIVALENT
    # =========================================

    @property
    def balance_tzs(self):

        if self.currency == "USD":

            return (
                self.balance *
                self.exchange_rate
            )

        return self.balance
    def save(self, *args, **kwargs):

        # GENERATE PURCHASE NUMBER

        if not self.purchase_number:

            year = timezone.now().year

            last_purchase = (
                Purchase.objects.filter(purchase_number__startswith=f"PUR-{year}")
                .order_by("-id")
                .first()
            )

            if last_purchase:

                last_number = int(last_purchase.purchase_number.split("-")[-1])

                new_number = last_number + 1

            else:

                new_number = 1

            self.purchase_number = f"PUR-{year}-{new_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):

        return self.purchase_number


class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="items"
    )

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="purchase_items"
    )

    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:

        ordering = ["id"]

    @property
    def subtotal(self):

        return self.quantity * self.unit_cost

    def __str__(self):

        return f"{self.product.product_name}"


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
        Purchase, on_delete=models.CASCADE, related_name="payments"
    )
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
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

    # =========================================
    # UPDATE PURCHASE TOTALS
    # =========================================

    def update_purchase_payment_status(self):

        self.update_purchase_totals(self.purchase)

    @staticmethod
    def update_purchase_totals(purchase):

        total_paid = (
            purchase.payments.aggregate(total=models.Sum("amount"))["total"] or 0
        )

        purchase.amount_paid = total_paid

        purchase.balance = purchase.total_amount - total_paid

        # PAYMENT STATUS

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

        ("tax", "Import Tax"),

        ("clearing", "Clearing Charges"),

        ("port", "Port Charges"),

        ("transport", "Local Transport"),

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

        related_name="additional_costs"

    )

    clearing_agent = models.ForeignKey(

        ClearingAgent,

        on_delete=models.SET_NULL,

        blank=True,

        null=True,

        related_name="costs"

    )

    cost_type = models.CharField(

        max_length=50,

        choices=COST_TYPES

    )

    description = models.CharField(

        max_length=255,

        blank=True,

        null=True

    )

    amount = models.DecimalField(

        max_digits=12,

        decimal_places=2

    )

    currency = models.CharField(

        max_length=10,

        choices=(
            ("USD", "USD"),
            ("TZS", "TZS"),
        ),

        default="TZS"

    )

    exchange_rate = models.DecimalField(

        max_digits=12,

        decimal_places=2,

        default=1

    )

    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS,

        default="pending"

    )

    notes = models.TextField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["id"]

    @property
    def amount_tzs(self):

        if self.currency == "USD":

            return (
                self.amount *
                self.exchange_rate
            )

        return self.amount

    def __str__(self):

        return (
            f"{self.get_cost_type_display()}"
        )