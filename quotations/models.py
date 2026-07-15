from decimal import Decimal

from django.db import models
from django.db.models import Sum

from customers.models import Customer
from products.models import Product


# =========================================
# PAYMENT TERM
# =========================================


class PaymentTerm(models.Model):

    term = models.CharField(
        max_length=300,
    )

    is_default = models.BooleanField(
        default=False,
    )


    class Meta:

        ordering = [
            "term",
        ]


    def __str__(self):

        return self.term


# =========================================
# QUOTATION
# =========================================


class Quotation(models.Model):

    TIME_UNIT_CHOICES = (
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("months", "Months"),
    )


    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quotations",
    )

    quote_date = models.DateField()

    due_date = models.DateField()


    # =========================================
    # COMPLETION PERIOD
    # =========================================

    completion_period_from = (
        models.PositiveIntegerField(
            default=0,
        )
    )

    completion_period_to = (
        models.PositiveIntegerField(
            default=0,
        )
    )

    completion_period_unit = models.CharField(
        max_length=10,
        choices=TIME_UNIT_CHOICES,
        default="days",
    )


    # =========================================
    # TERMS
    # =========================================

    payment_terms = models.ManyToManyField(
        PaymentTerm,
        blank=True,
        related_name="quotations",
    )
    # =========================================
    # TIMESTAMPS
    # =========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:

        ordering = [
            "-id",
        ]


    def __str__(self):

        return self.title


    # =========================================
    # TOTAL AMOUNT
    # ALL QUOTATION ITEMS
    # =========================================

    @property
    def total_amount(self):

        return sum(
            (
                item.total
                for item in self.items.all()
            ),
            Decimal("0"),
        )


    # =========================================
    # DELIVERABLE ITEMS
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def deliverable_items(self):

        return self.items.filter(
            is_tangible=True,
        )


    # =========================================
    # QUOTED DELIVERY QUANTITY
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def quoted_quantity(self):

        return (
            self.deliverable_items
            .aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


    # =========================================
    # DELIVERED QUANTITY
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def delivered_quantity(self):

        return sum(
            (
                item.delivered_quantity
                for item in self.deliverable_items
            ),
            Decimal("0"),
        )


    # =========================================
    # REMAINING QUANTITY
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def remaining_quantity(self):

        return sum(
            (
                item.remaining_quantity
                for item in self.deliverable_items
            ),
            Decimal("0"),
        )


    # =========================================
    # DELIVERY PERCENTAGE
    # =========================================

    @property
    def delivery_percentage(self):

        quoted_quantity = (
            self.quoted_quantity
        )


        if quoted_quantity <= Decimal("0"):

            return 0


        percentage = (
            self.delivered_quantity
            / quoted_quantity
        ) * Decimal("100")


        return round(
            percentage,
            2,
        )


    # =========================================
    # DELIVERY STATUS
    # =========================================

    @property
    def delivery_status(self):

        deliverable_items = (
            self.deliverable_items
        )


        # =====================================
        # NO PHYSICAL ITEMS
        # =====================================

        if not deliverable_items.exists():

            return "Not Applicable"


        # =====================================
        # NOTHING DELIVERED
        # =====================================

        if (
            self.delivered_quantity
            <= Decimal("0")
        ):

            return "Pending"


        # =====================================
        # EVERYTHING DELIVERED
        # =====================================

        if (
            self.remaining_quantity
            <= Decimal("0")
        ):

            return "Completed"


        # =====================================
        # PARTIAL DELIVERY
        # =====================================

        return "Partial"


# =========================================
# QUOTATION ITEM
# =========================================


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items",
    )


    # =========================================
    # PRODUCT
    # =========================================

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="quotation_items",
        blank=True,
        null=True,
    )


    # =========================================
    # CUSTOM ITEM
    # =========================================

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )


    # =========================================
    # QUANTITY
    # =========================================

    quantity = models.PositiveIntegerField(
        default=1,
    )


    # =========================================
    # UNIT PRICE
    # =========================================

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )


    # =========================================
    # DELIVERY STATE
    # =========================================

    is_tangible = models.BooleanField(
        default=True,
    )


    class Meta:

        ordering = [
            "id",
        ]


    def __str__(self):

        return self.item_name


    # =========================================
    # ITEM NAME
    # =========================================

    @property
    def item_name(self):

        if self.product:

            return (
                self.product.product_name
            )


        return (
            self.description
            or ""
        )


    # =========================================
    # TOTAL
    # ALL ITEMS HAVE FINANCIAL VALUE
    # =========================================

    @property
    def total(self):

        return (
            self.quantity
            * self.unit_price
        )


    # =========================================
    # DELIVERED QUANTITY
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def delivered_quantity(self):

        if not self.is_tangible:

            return Decimal("0")


        return (
            self.delivery_items
            .aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


    # =========================================
    # REMAINING QUANTITY
    # TANGIBLE ITEMS ONLY
    # =========================================

    @property
    def remaining_quantity(self):

        if not self.is_tangible:

            return Decimal("0")


        remaining = (
            self.quantity
            - self.delivered_quantity
        )


        return max(
            remaining,
            Decimal("0"),
        )


    # =========================================
    # FULLY DELIVERED
    # =========================================

    @property
    def is_fully_delivered(self):

        # =====================================
        # NON-TANGIBLE ITEMS DO NOT REQUIRE
        # DELIVERY
        # =====================================

        if not self.is_tangible:

            return True


        return (
            self.remaining_quantity
            <= Decimal("0")
        )


    # =========================================
    # DELIVERY PERCENTAGE
    # =========================================

    @property
    def delivery_percentage(self):

        # =====================================
        # NON-TANGIBLE ITEMS ARE NOT TRACKED
        # =====================================

        if not self.is_tangible:

            return 100


        if self.quantity <= Decimal("0"):

            return 0


        percentage = (
            self.delivered_quantity
            / self.quantity
        ) * Decimal("100")


        return round(
            percentage,
            2,
        )


    # =========================================
    # SAVE
    # =========================================

    def save(self, *args, **kwargs):

        # =====================================
        # PRODUCT ITEM
        # =====================================

        if self.product:

            # ---------------------------------
            # PRODUCT IS THE ITEM SOURCE
            # ---------------------------------

            self.description = None


            # ---------------------------------
            # COPY PRODUCT DELIVERY STATE
            # ---------------------------------

            self.is_tangible = (
                self.product.is_tangible
            )


        # =====================================
        # CUSTOM ITEM
        # =====================================

        else:

            self.product = None


        super().save(
            *args,
            **kwargs,
        )