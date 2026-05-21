# views.py

from decimal import Decimal
import json

from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.http import HttpResponse

from .models import *
from products.models import Product

from .forms import *

# =========================================
# PURCHASE LIST
# =========================================

def purchase_list(request):

    purchases = Purchase.objects.select_related(
        "supplier"
    ).all()

    context = {
        "purchases": purchases
    }

    return render(
        request,
        "purchases/purchase_list.html",
        context
    )


# =========================================
# PURCHASE TABLE PARTIAL
# =========================================

def purchase_table(request):

    purchases = Purchase.objects.select_related(
        "supplier"
    ).all()

    context = {
        "purchases": purchases
    }

    return render(
        request,
        "purchases/partials/purchase_table.html",
        context
    )


# =========================================
# CREATE PURCHASE
# =========================================

def purchase_create(request):

    form = PurchaseForm(
        request.POST or None
    )

    formset = PurchaseItemFormSet(
        request.POST or None,
        prefix="items"
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # CREATE PURCHASE

            purchase = form.save(commit=False)

            purchase.subtotal = Decimal("0.00")
            purchase.total_amount = Decimal("0.00")
            purchase.balance = Decimal("0.00")

            purchase.save()

            # SAVE ITEMS

            formset.instance = purchase

            items = formset.save(commit=False)

            subtotal = Decimal("0.00")

            for item in items:

                item.purchase = purchase

                item.save()

                subtotal += item.subtotal

            # UPDATE TOTALS

            purchase.subtotal = subtotal

            purchase.total_amount = subtotal

            purchase.balance = (
                subtotal - purchase.amount_paid
            )

            # PAYMENT STATUS

            if purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"

            purchase.save()

            # EMPTY RESPONSE

            response = HttpResponse("")

            # HTMX EVENTS

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True

            })

            return response

    context = {
        "form": form,
        "formset": formset,
        "products": Product.objects.filter(
            status="active"
        )
    }

    return render(
        request,
        "purchases/partials/purchase_form.html",
        context
    )


# =========================================
# UPDATE PURCHASE
# =========================================

def purchase_update(request, pk):

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    form = PurchaseForm(
        request.POST or None,
        instance=purchase
    )

    formset = PurchaseItemFormSet(
        request.POST or None,
        instance=purchase,
        prefix="items"
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            purchase = form.save(commit=False)

            # SAVE FORMSET

            formset.instance = purchase

            formset.save()


            # RECALCULATE SUBTOTAL FROM DATABASE

            subtotal = Decimal("0.00")

            for item in purchase.items.all():

                subtotal += item.subtotal


            # UPDATE TOTALS

            purchase.subtotal = subtotal

            purchase.total_amount = subtotal

            purchase.balance = (
                purchase.total_amount -
                purchase.amount_paid
            )


            # PAYMENT STATUS

            if purchase.total_amount <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"


            purchase.save()


            # EMPTY RESPONSE

            response = HttpResponse("")


            # HTMX EVENTS

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True

            })

            return response

    context = {

        "form": form,

        "formset": formset,

        "purchase": purchase,

        "products": Product.objects.filter(
            status="active"
        )

    }

    return render(

        request,

        "purchases/partials/purchase_form.html",

        context

    )

# =========================================
# DELETE PURCHASE
# =========================================

def purchase_delete(request, pk):

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    if request.method == "POST":

        purchase.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps({

            "purchaseChanged": True,

            "closeModal": True

        })

        return response

    context = {
        "purchase": purchase
    }

    return render(
        request,
        "purchases/partials/purchase_delete.html",
        context
    )
    
# =========================================
# CREATE PAYMENT
# =========================================

def purchase_payment_create(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    form = PurchasePaymentForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            payment = form.save(commit=False)

            payment.purchase = purchase

            payment.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True

            })

            return response

    context = {

        "form": form,

        "purchase": purchase

    }

    return render(

        request,

        "purchases/payments/payment_form.html",

        context

    )