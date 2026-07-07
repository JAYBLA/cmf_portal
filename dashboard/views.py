from datetime import date

from django.db.models import (
    Avg,
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Sum,
)
from django.db.models.functions import ExtractMonth
from django.shortcuts import render

from customers.models import Customer
from dashboard.financials import chart_data
from invoices.models import Invoice
from products.models import Product
from quotations.models import Quotation
from receipts.models import Receipt
from sales.models import Sale, SaleItem
from vouchers.models import Voucher


def dashboard(request):

    # =========================================
    # CURRENT DATE
    # =========================================

    today = date.today()

    current_year = today.year
    current_month = today.month


    # =========================================
    # SELECTED YEAR
    # =========================================

    try:

        selected_year = int(
            request.GET.get(
                "year",
                current_year,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        selected_year = current_year


    # =========================================
    # AVAILABLE YEARS
    # =========================================

    sale_years = (
        Sale.objects
        .dates(
            "sale_date",
            "year",
            order="DESC",
        )
    )


    available_years = {
        year.year
        for year in sale_years
    }


    # =========================================
    # INCLUDE CURRENT YEAR
    # =========================================

    available_years.add(
        current_year
    )


    # =========================================
    # INCLUDE SELECTED YEAR
    # =========================================

    available_years.add(
        selected_year
    )


    available_years = sorted(
        available_years,
        reverse=True,
    )


    # =========================================
    # DASHBOARD COUNTS
    # =========================================

    customers_count = (
        Customer.objects.count()
    )

    quotation_count = (
        Quotation.objects.count()
    )

    invoice_count = (
        Invoice.objects.count()
    )

    receipt_count = (
        Receipt.objects.count()
    )

    voucher_count = (
        Voucher.objects.count()
    )


    # =========================================
    # FINANCIAL CHART DATA
    # =========================================

    financial = chart_data(
        selected_year
    )


    # =========================================
    # MONTHLY SALES
    # JANUARY - DECEMBER
    # =========================================

    monthly_sales = (
        Sale.objects
        .filter(
            status="confirmed",
            sale_date__year=selected_year,
        )
        .annotate(
            month=ExtractMonth(
                "sale_date"
            )
        )
        .values(
            "month"
        )
        .annotate(
            total=Sum(
                "total_amount"
            )
        )
        .order_by(
            "month"
        )
    )


    sales_chart = [
        0
    ] * 12


    for row in monthly_sales:

        sales_chart[
            row["month"] - 1
        ] = float(
            row["total"]
            or 0
        )


    # =========================================
    # TOTAL SALES FOR SELECTED YEAR
    # =========================================

    yearly_sales = (
        Sale.objects
        .filter(
            status="confirmed",
            sale_date__year=selected_year,
        )
        .aggregate(
            total=Sum(
                "total_amount"
            )
        )["total"]
        or 0
    )


    # =========================================
    # MONTHLY TOTAL
    # =========================================
    # CURRENT YEAR:
    # CURRENT MONTH
    #
    # PREVIOUS YEAR:
    # SAME MONTH AS CURRENT MONTH
    # =========================================

    monthly_total = (
        Sale.objects
        .filter(
            status="confirmed",
            sale_date__year=selected_year,
            sale_date__month=current_month,
        )
        .aggregate(
            total=Sum(
                "total_amount"
            )
        )["total"]
        or 0
    )


    # =========================================
    # PREVIOUS YEAR TOTAL SALES
    # =========================================

    previous_year_total = (
        Sale.objects
        .filter(
            status="confirmed",
            sale_date__year=(
                selected_year - 1
            ),
        )
        .aggregate(
            total=Sum(
                "total_amount"
            )
        )["total"]
        or 0
    )


    # =========================================
    # SALES GROWTH
    # =========================================

    if previous_year_total > 0:

        sales_growth = round(
            (
                (
                    float(yearly_sales)
                    - float(
                        previous_year_total
                    )
                )
                / float(
                    previous_year_total
                )
            )
            * 100,
            1,
        )

    else:

        sales_growth = 0


    # =========================================
    # TOP SELLING PRODUCTS
    # SELECTED YEAR
    # =========================================

    top_selling_products = (
        SaleItem.objects
        .filter(
            sale__status="confirmed",
            sale__sale_date__year=(
                selected_year
            ),
        )
        .annotate(
            line_total=ExpressionWrapper(
                F("quantity")
                * F("unit_price"),
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
            unit_price=Avg(
                "unit_price"
            ),
            total_sold=Sum(
                "quantity"
            ),
            total_orders=Count(
                "sale",
                distinct=True,
            ),
            total_revenue=Sum(
                "line_total"
            ),
        )
        .order_by(
            "-total_sold"
        )[:10]
    )


    # =========================================
    # STOCK REPORT
    # =========================================

    stock_report = (
        Product.objects
        .select_related(
            "product_category"
        )
        .prefetch_related(
            "sales_pricing"
        )
        .order_by(
            "product_name"
        )[:10]
    )


    # =========================================
    # CONTEXT
    # =========================================

    context = {

        # -------------------------------------
        # DASHBOARD COUNTS
        # -------------------------------------

        "customers_count": (
            customers_count
        ),

        "quotation_count": (
            quotation_count
        ),

        "invoice_count": (
            invoice_count
        ),

        "receipt_count": (
            receipt_count
        ),

        "voucher_count": (
            voucher_count
        ),


        # -------------------------------------
        # YEAR FILTER
        # -------------------------------------

        "current_year": (
            current_year
        ),

        "selected_year": (
            selected_year
        ),

        "available_years": (
            available_years
        ),


        # -------------------------------------
        # SALES
        # -------------------------------------

        "sales_chart": (
            sales_chart
        ),

        "yearly_sales": (
            yearly_sales
        ),

        "monthly_total": (
            monthly_total
        ),

        "sales_growth": (
            sales_growth
        ),


        # -------------------------------------
        # TOP SELLING PRODUCTS
        # -------------------------------------

        "top_selling_products": (
            top_selling_products
        ),


        # -------------------------------------
        # STOCK REPORT
        # -------------------------------------

        "stock_report": (
            stock_report
        ),

    }


    # =========================================
    # FINANCIAL DASHBOARD DATA
    # =========================================

    context.update(
        financial
    )


    # =========================================
    # RENDER DASHBOARD
    # =========================================

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )