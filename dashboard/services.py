from decimal import Decimal
from datetime import date

from django.db.models import Sum

from sales.models import Sale
from purchases.models import Purchase


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

def monthly_purchases(year=None):
    """
    Returns monthly purchase totals in TZS.
    """

    if year is None:
        year = date.today().year

    months = [Decimal("0")] * 12

    queryset = (
        Purchase.objects
        .filter(
            purchase_date__year=year,
        )
        .values("purchase_date__month")
        .annotate(
            total=Sum("total_amount_tzs")
        )
    )

    for row in queryset:
        months[row["purchase_date__month"] - 1] = row["total"] or Decimal("0")

    return months