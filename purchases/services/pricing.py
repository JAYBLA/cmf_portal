from decimal import Decimal

from ..models import PurchaseProductPricing
from sales.services.pricing import (
    update_selling_price,
)


def recalculate_purchase_pricing(purchase):

    items = purchase.items.all()

    if not items.exists():
        return

    total_purchase_value = Decimal("0.00")
    item_values = {}

    # ==========================
    # PURCHASE VALUE
    # ==========================

    for item in items:

        if purchase.currency == "USD":

            value = (
                item.subtotal *
                purchase.exchange_rate
            )

        else:

            value = item.subtotal

        item_values[item.id] = value
        total_purchase_value += value

    # ==========================
    # TOTAL EXTRA COSTS
    # ==========================

    total_extra_costs = Decimal("0.00")

    for cost in purchase.additional_costs.filter(
        payment_status="paid"
    ):
        total_extra_costs += cost.amount_tzs

    # ==========================
    # ALLOCATE COSTS
    # ==========================

    for item in items:

        purchase_value = item_values[item.id]

        percentage = Decimal("0.00")

        if total_purchase_value > 0:

            percentage = (
                purchase_value /
                total_purchase_value
            )

        allocated_cost = (
            total_extra_costs *
            percentage
        )

        landed_total = (
            purchase_value +
            allocated_cost
        )

        landed_unit = Decimal("0.00")

        if item.quantity > 0:

            landed_unit = (
                landed_total /
                item.quantity
            )

        purchase_pricing, created = (
            PurchaseProductPricing.objects.update_or_create(
                purchase_item=item,
                defaults={
                    "product": item.product,
                    "purchase": purchase,
                    "quantity": item.quantity,
                    "purchase_value_tzs": purchase_value,
                    "allocated_cost_tzs": allocated_cost,
                    "landed_cost_total": landed_total,
                    "landed_unit_cost": landed_unit,
                }
            )
        )

        update_selling_price(
            purchase_pricing
        )