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

                item.product.update_stock(
                    quantity=item.quantity,
                    movement_type="out",
                    reference=sale.sale_number,
                    notes="Sales Stock Out",
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

                old_item.product.update_stock(
                    quantity=old_item.quantity,
                    movement_type="in",
                    reference=sale.sale_number,
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

                item.product.update_stock(
                    quantity=item.quantity,
                    movement_type="out",
                    reference=sale.sale_number,
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

            item.product.update_stock(
                quantity=item.quantity,
                movement_type="in",
                reference=sale.sale_number,
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

    product = get_object_or_404(Product, pk=product_id)

    selling_price = Decimal("0.00")

    if hasattr(product, "sales_pricing"):

        selling_price = product.sales_pricing.selling_price

    return JsonResponse(
        {"product_id": product.id, "selling_price": float(selling_price)}
    )
