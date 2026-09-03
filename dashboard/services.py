from datetime import date
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import ExtractMonth

from expenses.models import Expense
from projects.models import ProjectExpense
from purchases.models import PurchaseAdditionalCost, PurchasePayment
from receipts.models import Receipt
from sales.models import SalePayment
from vouchers.models import Voucher


ZERO = Decimal("0.00")


def _empty_months():
    return [ZERO for _ in range(12)]


def _add_grouped_amount(months, queryset, date_field, amount_field="amount"):
    rows = (
        queryset.annotate(month=ExtractMonth(date_field))
        .values("month")
        .annotate(total=Sum(amount_field))
    )
    for row in rows:
        if row["month"]:
            months[row["month"] - 1] += row["total"] or ZERO


def monthly_income(year=None):
    """Return actual cash received without counting mirrored payments twice."""
    year = year or date.today().year
    months = _empty_months()

    _add_grouped_amount(
        months,
        Receipt.objects.filter(receipt_date__year=year),
        "receipt_date",
    )
    _add_grouped_amount(
        months,
        SalePayment.objects.filter(
            payment_date__year=year,
            sale__source_invoice__isnull=True,
            sale__status="confirmed",
        ),
        "payment_date",
    )
    return months


def monthly_expenses(year=None):
    """Return actual or explicitly paid money-out records in TZS."""
    year = year or date.today().year
    months = _empty_months()

    for payment in PurchasePayment.objects.filter(
        payment_date__year=year
    ).select_related("purchase"):
        amount_tzs = payment.amount
        if payment.purchase.currency == "USD":
            amount_tzs *= payment.purchase.exchange_rate
        months[payment.payment_date.month - 1] += amount_tzs

    # Additional costs have no payment-date field, so their purchase date is
    # the only reliable accounting date currently available.
    for cost in PurchaseAdditionalCost.objects.filter(
        payment_status="paid",
        purchase__purchase_date__year=year,
    ).select_related("purchase"):
        months[cost.purchase.purchase_date.month - 1] += cost.amount_tzs

    _add_grouped_amount(
        months,
        Voucher.objects.filter(status="paid", voucher_date__year=year),
        "voucher_date",
        "total_amount",
    )
    _add_grouped_amount(
        months,
        ProjectExpense.objects.filter(expense_date__year=year),
        "expense_date",
    )
    _add_grouped_amount(
        months,
        Expense.objects.filter(expense_date__year=year),
        "expense_date",
    )
    return months


# Preserve the former service API for any callers outside the dashboard.
monthly_sales = monthly_income
monthly_purchases = monthly_expenses


def financial_years():
    """Return every year represented by an income or money-out source."""
    sources = (
        (Receipt.objects.all(), "receipt_date"),
        (SalePayment.objects.filter(sale__source_invoice__isnull=True), "payment_date"),
        (PurchasePayment.objects.all(), "payment_date"),
        (PurchaseAdditionalCost.objects.filter(payment_status="paid"), "purchase__purchase_date"),
        (Voucher.objects.filter(status="paid"), "voucher_date"),
        (ProjectExpense.objects.all(), "expense_date"),
        (Expense.objects.all(), "expense_date"),
    )
    years = set()
    for queryset, field in sources:
        years.update(value.year for value in queryset.dates(field, "year"))
    return years
