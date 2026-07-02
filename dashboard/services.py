from decimal import Decimal
from datetime import date

from django.db.models import Sum

from sales.models import Sale
from purchases.models import *


# ==========================================================
# SALES
# ==========================================================

def monthly_sales(year=None):
    """
    Returns monthly confirmed sales totals.
    """

    if year is None:
        year = date.today().year

    months = [Decimal("0")] * 12

    queryset = (
        Sale.objects
        .filter(
            status="confirmed",
            sale_date__year=year,
        )
        .values("sale_date__month")
        .annotate(total=Sum("total_amount"))
    )

    for row in queryset:
        months[row["sale_date__month"] - 1] = row["total"] or Decimal("0")

    return months


# ==========================================================
# PURCHASES
# ==========================================================

def monthly_purchases(year):
    monthly = []

    for month in range(1, 13):

        purchases_total = (
            Purchase.objects.filter(
                purchase_date__year=year,
                purchase_date__month=month,
            ).aggregate(total=Sum("total_amount_tzs"))["total"]
            or Decimal("0")
        )

        additional_total = Decimal("0")

        costs = PurchaseAdditionalCost.objects.filter(
            purchase__purchase_date__year=year,
            purchase__purchase_date__month=month,
        )

        for cost in costs:
            additional_total += cost.amount_tzs

        monthly.append(purchases_total + additional_total)

    return monthly