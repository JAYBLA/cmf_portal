from sales.models import SalesProductPricing


def update_selling_price(
    purchase_pricing
):
    """
    Create or update selling price
    from landed cost.
    """

    obj, created = (
        SalesProductPricing.objects.update_or_create(
            product=purchase_pricing.product,
            defaults={
                "purchase_pricing": purchase_pricing,
                "landed_unit_cost":
                    purchase_pricing.landed_unit_cost,
            }
        )
    )

    obj.save()

    return obj