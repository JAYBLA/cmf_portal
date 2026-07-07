from decimal import Decimal
import json

from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.http import (
    HttpResponse,
    JsonResponse,
)

from django.db.models import Sum

from .models import *
from .forms import *

from products.models import Product
from products.services.stock import move_stock

# =========================================
# SALE LIST
# =========================================


def sale_list(request):

    sales = Sale.objects.select_related("customer").all()

    context = {
        "sales": sales,
    }

    return render(request, "sales/sales_list.html", context)


# =========================================
# SALE TABLE
# =========================================


def sale_table(request):

    sales = Sale.objects.select_related("customer").all()

    context = {
        "sales": sales,
    }

    return render(request, "sales/partials/sale_table.html", context)


# =========================================
# CREATE SALE
# =========================================


def sale_create(request):

    form = SaleForm(request.POST or None)

    formset = SaleItemFormSet(request.POST or None, prefix="items")

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            sale = form.save(commit=False)

            sale.subtotal = Decimal("0.00")
            sale.total_amount = Decimal("0.00")
            sale.balance = Decimal("0.00")

            sale.save()

            formset.instance = sale

            items = formset.save(commit=False)

            for item in items:

                item.sale = sale

                item.save()

                move_stock(
                    product=item.product,
                    quantity=item.quantity,
                    direction="out",
                    movement_type="sale",
                    reference=sale,
                    notes="Sale",
                )

            for obj in formset.deleted_objects:

                obj.delete()

            subtotal = Decimal("0.00")

            for item in sale.items.all():

                subtotal += item.subtotal

            sale.subtotal = subtotal
            sale.total_amount = subtotal
            sale.balance = sale.total_amount - sale.amount_paid

            sale.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Sale saved successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "products": Product.objects.filter(status="active"),
    }

    return render(request, "sales/partials/sales_form.html", context)


# =========================================
# UPDATE SALE
# =========================================


def sale_update(request, pk):

    sale = get_object_or_404(Sale, pk=pk)

    form = SaleForm(request.POST or None, instance=sale)

    formset = SaleItemFormSet(request.POST or None, instance=sale, prefix="items")

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            for old_item in sale.items.all():

                move_stock(
                    product=old_item.product,
                    quantity=old_item.quantity,
                    direction="in",
                    movement_type="sale",
                    reference=sale,
                    notes="Sale Update Reversal",
                )

            sale = form.save(commit=False)

            sale.save()

            formset.instance = sale

            items = formset.save(commit=False)

            for obj in formset.deleted_objects:

                obj.delete()

            for item in items:

                item.sale = sale

                item.save()

                move_stock(
                    product=item.product,
                    quantity=item.quantity,
                    direction="out",
                    movement_type="sale",
                    reference=sale,
                    notes="Sale Update",
                )

            subtotal = Decimal("0.00")

            for item in sale.items.all():

                subtotal += item.subtotal

            sale.subtotal = subtotal
            sale.total_amount = subtotal

            sale.balance = sale.total_amount - sale.amount_paid

            if sale.amount_paid <= 0:

                sale.payment_status = "pending"

            elif sale.amount_paid < sale.total_amount:

                sale.payment_status = "partial"

            else:

                sale.payment_status = "paid"

            sale.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Sale updated successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "sale": sale,
    }

    return render(request, "sales/partials/sales_form.html", context)


# =========================================
# DELETE SALE
# =========================================


def sale_delete(request, pk):

    sale = get_object_or_404(Sale, pk=pk)

    if request.method == "POST":

        for item in sale.items.all():

            move_stock(
                product=item.product,
                quantity=item.quantity,
                direction="in",
                movement_type="sale",
                reference=sale,
                notes="Sale Deleted",
            )
        sale.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": ("Sale deleted successfully."),
                },
            }
        )

        return response

    context = {
        "sale": sale,
    }

    return render(request, "sales/partials/sales_delete.html", context)


# =========================================
# CREATE SALE PAYMENT
# =========================================


def sale_payment_create(request, sale_id):

    sale = get_object_or_404(Sale, pk=sale_id)

    form = SalePaymentForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            payment = form.save(commit=False)

            payment.sale = sale

            payment.save()

            total_paid = sale.payments.aggregate(total=Sum("amount"))[
                "total"
            ] or Decimal("0.00")

            sale.amount_paid = total_paid

            sale.balance = sale.total_amount - sale.amount_paid

            if sale.amount_paid <= 0:

                sale.payment_status = "pending"

            elif sale.amount_paid < sale.total_amount:

                sale.payment_status = "partial"

            else:

                sale.payment_status = "paid"

            sale.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Sale payment recorded successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "sale": sale,
    }

    return render(request, "sales/payments/payment_form.html", context)


# =========================================
# PRODUCT PRICE
# =========================================


def product_price(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id,
    )

    calculated_price = Decimal("0.00")
    declared_price = None
    effective_price = Decimal("0.00")

    if hasattr(product, "sales_pricing"):

        pricing = product.sales_pricing

        calculated_price = pricing.selling_price
        declared_price = pricing.declared_price
        effective_price = pricing.effective_selling_price

    return JsonResponse(
        {
            "product_id": product.id,
            "calculated_price": float(calculated_price),
            "declared_price": (
                float(declared_price) if declared_price is not None else None
            ),
            "selling_price": float(effective_price),
        }
    )


def sale_detail(request, pk):
    sale = get_object_or_404(
        Sale.objects.prefetch_related("items__product", "payments"), pk=pk
    )
    return render(
        request,
        "sales/partials/sale_detail.html",
        {
            "sale": sale,
        },
    )


# =========================================
# DECLARED PRICE LIST
# =========================================


def declared_price_list(request):

    prices = SalesProductPricing.objects.select_related(
        "product",
        "purchase_pricing",
    ).filter(
        declared_price__isnull=False,
    )

    context = {
        "prices": prices,
    }

    return render(
        request,
        "sales/pricing/list.html",
        context,
    )


# =========================================
# DECLARED PRICE TABLE
# =========================================


def declared_price_table(request):

    prices = SalesProductPricing.objects.select_related(
        "product",
        "purchase_pricing",
    ).filter(
        declared_price__isnull=False,
    )

    context = {
        "prices": prices,
    }

    return render(
        request,
        "sales/pricing/table.html",
        context,
    )


# =========================================
# CREATE DECLARED PRICE
# =========================================


def declared_price_create(request):

    form = DeclaredPriceForm(
        request.POST or None,
    )

    if request.method == "POST":

        if form.is_valid():

            product = form.cleaned_data[
                "product"
            ]

            declared_price = form.cleaned_data[
                "declared_price"
            ]

            pricing = get_object_or_404(
                SalesProductPricing,
                product=product,
            )

            pricing.declared_price = declared_price

            pricing.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": (
                            "Declared price added "
                            "successfully."
                        ),
                    },
                }
            )

            return response

    context = {
        "form": form,
    }

    return render(
        request,
        "sales/pricing/form.html",
        context,
    )


# =========================================
# UPDATE DECLARED PRICE
# =========================================


def declared_price_update(request, pk):

    pricing = get_object_or_404(
        SalesProductPricing,
        pk=pk,
    )

    form = DeclaredPriceForm(
        request.POST or None,
        pricing=pricing,
    )

    if request.method == "POST":

        if form.is_valid():

            pricing.declared_price = (
                form.cleaned_data["declared_price"]
            )

            pricing.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": (
                            "Declared price updated "
                            "successfully."
                        ),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "pricing": pricing,
    }

    return render(
        request,
        "sales/pricing/form.html",
        context,
    )

# =========================================
# DELETE DECLARED PRICE
# =========================================


def declared_price_delete(request, pk):

    pricing = get_object_or_404(
        SalesProductPricing,
        pk=pk,
    )

    if request.method == "POST":

        pricing.declared_price = None

        pricing.save()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": ("Declared price removed " "successfully."),
                },
            }
        )

        return response

    context = {
        "pricing": pricing,
    }

    return render(
        request,
        "sales/pricing/delete.html",
        context,
    )
    
# =====================================================
# SALE DETAIL
# =====================================================


def sale_detail(request, pk):

    # =========================================
    # GET SALE
    # =========================================

    sale = get_object_or_404(

        Sale.objects.select_related(

            "customer",

        ).prefetch_related(

            "items__product",

            "payments",

        ),

        pk=pk,

    )


    # =========================================
    # CONTEXT
    # =========================================

    context = {

        "sale": sale,

    }


    # =========================================
    # RENDER DETAIL
    # =========================================

    return render(

        request,

        "sales/sale_detail.html",

        context,

    )
