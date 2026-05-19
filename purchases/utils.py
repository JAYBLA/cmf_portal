from .models import Purchase


def generate_purchase_number():

    last_purchase = Purchase.objects.order_by(
        "-id"
    ).first()

    if last_purchase:

        last_id = last_purchase.id + 1

    else:

        last_id = 1

    return f"PUR-{last_id:05d}"