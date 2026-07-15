from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from quotations.models import (
    Quotation,
    QuotationItem,
)


# =========================================
# DELIVERY NOTE
# =========================================


class DeliveryNote(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("partial", "Partially Delivered"),
        ("completed", "Completed"),
    )

    delivery_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.PROTECT,
        related_name="delivery_notes",
    )

    delivery_date = models.DateField()

    delivery_address = models.TextField(
        blank=True,
    )

    receiver_name = models.CharField(
        max_length=255,
        blank=True,
    )

    receiver_phone = models.CharField(
        max_length=50,
        blank=True,
    )

    driver_name = models.CharField(
        max_length=255,
        blank=True,
    )

    vehicle_number = models.CharField(
        max_length=100,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

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

        return self.delivery_number


    # =========================================
    # CUSTOMER
    # =========================================

    @property
    def customer(self):

        return self.quotation.customer


    # =========================================
    # DELIVERABLE QUOTATION ITEMS
    # =========================================

    @property
    def deliverable_quotation_items(self):

        return (
            self.quotation.items
            .filter(
                product__is_tangible=True,
            )
        )


    # =========================================
    # QUOTED DELIVERABLE QUANTITY
    # =========================================

    @property
    def quoted_quantity(self):

        return (
            self.deliverable_quotation_items
            .aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


    # =========================================
    # CURRENT NOTE DELIVERED QUANTITY
    # =========================================

    @property
    def delivered_quantity(self):

        return (
            self.items
            .filter(
                quotation_item__product__is_tangible=True,
            )
            .aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


    # =========================================
    # TOTAL DELIVERABLE ITEMS
    # =========================================

    @property
    def total_items(self):

        return (
            self.items
            .filter(
                quotation_item__product__is_tangible=True,
            )
            .count()
        )


    # =========================================
    # TOTAL AMOUNT
    # =========================================

    @property
    def total_amount(self):

        return sum(
            (
                item.total_price
                for item in self.items.filter(
                    quotation_item__product__is_tangible=True,
                )
            ),
            Decimal("0"),
        )


    # =========================================
    # UPDATE DELIVERY STATUS
    # =========================================

    def update_delivery_status(self):

        # =====================================
        # TANGIBLE PRODUCTS ONLY
        # =====================================

        quotation_items = (
            self.deliverable_quotation_items
        )


        # =====================================
        # NO DELIVERABLE ITEMS
        # =====================================

        if not quotation_items.exists():

            self.status = "pending"

            self.save(
                update_fields=[
                    "status",
                ]
            )

            return


        has_delivery = False

        fully_delivered = True


        # =====================================
        # CHECK EACH TANGIBLE PRODUCT
        # =====================================

        for quotation_item in quotation_items:

            delivered = (
                quotation_item
                .delivery_items
                .aggregate(
                    total=Sum("quantity")
                )["total"]
                or Decimal("0")
            )


            if delivered > Decimal("0"):

                has_delivery = True


            if delivered < quotation_item.quantity:

                fully_delivered = False


        # =====================================
        # DETERMINE STATUS
        # =====================================

        if fully_delivered:

            self.status = "completed"

        elif has_delivery:

            self.status = "partial"

        else:

            self.status = "pending"


        # =====================================
        # SAVE STATUS
        # =====================================

        self.save(
            update_fields=[
                "status",
            ]
        )


    # =========================================
    # SAVE
    # =========================================

    def save(self, *args, **kwargs):

        if not self.delivery_number:

            today = timezone.now().strftime(
                "%Y%m%d"
            )

            last = (
                DeliveryNote.objects
                .filter(
                    delivery_number__startswith=(
                        f"DN-{today}"
                    )
                )
                .order_by("-id")
                .first()
            )


            if last:

                number = (
                    int(
                        last.delivery_number
                        .split("-")[-1]
                    )
                    + 1
                )

            else:

                number = 1


            self.delivery_number = (
                f"DN-{today}-{number:04d}"
            )


        super().save(
            *args,
            **kwargs,
        )


# =========================================
# DELIVERY NOTE ITEM
# =========================================


class DeliveryNoteItem(models.Model):

    delivery_note = models.ForeignKey(
        DeliveryNote,
        on_delete=models.CASCADE,
        related_name="items",
    )

    quotation_item = models.ForeignKey(
        QuotationItem,
        on_delete=models.PROTECT,
        related_name="delivery_items",
    )

    quantity = models.PositiveIntegerField(default=1)

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )


    class Meta:

        ordering = [
            "id",
        ]


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

        return (
            self.quantity
            * self.unit_price
        )


    # =========================================
    # TOTAL PREVIOUSLY DELIVERED
    # =========================================

    @property
    def previously_delivered_quantity(self):

        queryset = (
            self.quotation_item
            .delivery_items
            .all()
        )


        if self.pk:

            queryset = queryset.exclude(
                pk=self.pk
            )


        return (
            queryset.aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


    # =========================================
    # REMAINING QUANTITY
    # =========================================

    @property
    def remaining_quantity(self):

        return max(
            self.quoted_quantity
            - self.previously_delivered_quantity,
            Decimal("0"),
        )