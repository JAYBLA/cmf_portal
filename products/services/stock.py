from decimal import Decimal

from products.models import StockMovement

def move_stock(
    *,
    product,
    quantity,
    direction,
    movement_type,
    reference=None,
    notes="",
):

    quantity = Decimal(quantity)

    if direction == "in":
        new_balance = product.current_stock + quantity
    else:
        new_balance = product.current_stock - quantity

    product.current_stock = new_balance
    product.save(update_fields=["current_stock"])

    StockMovement.objects.create(
        product=product,
        quantity=quantity,
        direction=direction,
        movement_type=movement_type,
        balance_after=new_balance,
        reference=reference,
        remarks=notes,
    )