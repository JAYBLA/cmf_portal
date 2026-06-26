from django.shortcuts import render
from customers.models import *
from quotations.models import *
from invoices.models import *
from sales.models import Sale

from django.db.models.functions import *

from datetime import date
import json
from django.db.models import *
from sales.models import *


def dashboard(request):

    # Dashboard counts
    customers_count = Customer.objects.count()
    quotation_count = Quotation.objects.count()
    invoice_count = Invoice.objects.count()

    current_year = date.today().year
    current_month = date.today().month

    # ===========================
    # Monthly Sales Chart (Jan-Dec)
    # ===========================
    monthly_sales = (
        Sale.objects.filter(status="confirmed", sale_date__year=current_year)
        .annotate(month=ExtractMonth("sale_date"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    sales_chart = [0] * 12

    for row in monthly_sales:
        sales_chart[row["month"] - 1] = float(row["total"] or 0)

    # ===========================
    # Total Sales This Year
    # ===========================
    yearly_sales = (
        Sale.objects.filter(status="confirmed", sale_date__year=current_year).aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    # ===========================
    # Total Sales This Month
    # ===========================
    monthly_total = (
        Sale.objects.filter(
            status="confirmed",
            sale_date__year=current_year,
            sale_date__month=current_month,
        ).aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    # ===========================
    # Previous Year's Total Sales
    # ===========================
    previous_year_total = (
        Sale.objects.filter(
            status="confirmed", sale_date__year=current_year - 1
        ).aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    # ===========================
    # Growth Percentage
    # ===========================
    if previous_year_total > 0:
        sales_growth = round(
            (
                (float(yearly_sales) - float(previous_year_total))
                / float(previous_year_total)
            )
            * 100,
            1,
        )
    else:
        sales_growth = 0

    # ===========================
    # Top Selling Products
    # ===========================
    top_selling_products = (
        SaleItem.objects
        .filter(sale__status="confirmed")
        .annotate(
            line_total=ExpressionWrapper(
                F("quantity") * F("unit_price"),
                output_field=DecimalField(
                    max_digits=18,
                    decimal_places=2,
                ),
            )
        )
        .values(
            "product__id",
            "product__product_name",
            "product__product_category__name",
        )
        .annotate(
            unit_price=Avg("unit_price"),
            total_sold=Sum("quantity"),
            total_orders=Count("sale", distinct=True),
            total_revenue=Sum("line_total"),
        )
        .order_by("-total_sold")[:10]
    )
    
    # ===========================
    # Stock Report
    # ===========================
    stock_report = (
        Product.objects
        .select_related("product_category")
        .prefetch_related("sales_pricing")
        .order_by("product_name")[:10]
    )

    context = {
        # Counts
        "customers_count": customers_count,
        "quotation_count": quotation_count,
        "invoice_count": invoice_count,
        # Dashboard Sales Statistics
        "yearly_sales": float(yearly_sales),
        "monthly_total": float(monthly_total),
        "sales_growth": sales_growth,
        # ApexCharts data
        "sales_chart": json.dumps(sales_chart),
        # Current year
        "current_year": current_year,
        # Top Selling Products
        "top_selling_products": top_selling_products,
        # Stock Report
        "stock_report": stock_report
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
