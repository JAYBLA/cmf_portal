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
from django.db.models import Sum

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

            # =========================================
            # CREATE PURCHASE
            # =========================================

            purchase = form.save(commit=False)

            purchase.subtotal = Decimal("0.00")

            purchase.total_amount = Decimal("0.00")

            purchase.total_amount_tzs = Decimal("0.00")

            purchase.balance = Decimal("0.00")

            purchase.save()


            # =========================================
            # SAVE ITEMS
            # =========================================

            formset.instance = purchase

            items = formset.save(commit=False)

            subtotal = Decimal("0.00")

            for item in items:

                # =====================================
                # ASSIGN PURCHASE
                # =====================================

                item.purchase = purchase

                item.save()

                # =====================================
                # SUBTOTAL
                # =====================================

                subtotal += item.subtotal

                # =====================================
                # STOCK IN
                # =====================================

                item.product.update_stock(

                    quantity=item.quantity,

                    movement_type="in",

                    unit_cost=item.unit_cost,

                    reference=purchase.purchase_number,

                    notes="Purchase Stock In"

                )


            # =========================================
            # SHIPPING COSTS
            # =========================================

            international_shipping = (
                purchase.international_shipping_cost or
                Decimal("0.00")
            )

            local_shipping = (
                purchase.local_shipping_cost or
                Decimal("0.00")
            )


            # =========================================
            # TOTAL AMOUNT
            # =========================================

            if purchase.currency == "USD":

                # ONLY USD COMPONENTS

                purchase.total_amount = (

                    subtotal +

                    international_shipping

                )

            else:

                purchase.currency = "TZS"

                purchase.exchange_rate = 1

                purchase.total_amount = (

                    subtotal +

                    local_shipping

                )


            # =========================================
            # TZS EQUIVALENT
            # =========================================

            if purchase.currency == "USD":

                if purchase.exchange_rate <= 0:

                    purchase.exchange_rate = 1


                # ONLY USD PART IS CONVERTED

                usd_total = (

                    subtotal +

                    international_shipping

                )

                purchase.total_amount_tzs = (

                    usd_total *

                    purchase.exchange_rate

                ) + local_shipping

            else:

                # LOCAL PURCHASES

                purchase.currency = "TZS"

                purchase.exchange_rate = 1

                purchase.total_amount_tzs = (
                    purchase.total_amount
                )


            # =========================================
            # BALANCE
            # =========================================

            purchase.balance = (

                purchase.total_amount -

                purchase.amount_paid

            )


            # =========================================
            # PAYMENT STATUS
            # =========================================

            if purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"


            purchase.save()


            # =========================================
            # RESPONSE
            # =========================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Purchase saved successfully."
                    )

                }

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


            # =========================================
            # SAVE FORMSET
            # =========================================

            formset.instance = purchase

            formset.save()


            # =========================================
            # RECALCULATE SUBTOTAL
            # =========================================

            subtotal = Decimal("0.00")

            for item in purchase.items.all():

                subtotal += item.subtotal


            # =========================================
            # SHIPPING COSTS
            # =========================================

            international_shipping = (
                purchase.international_shipping_cost or
                Decimal("0.00")
            )

            local_shipping = (
                purchase.local_shipping_cost or
                Decimal("0.00")
            )


            # =========================================
            # TOTAL AMOUNT
            # =========================================

            if purchase.currency == "USD":

                # ONLY USD COMPONENTS

                purchase.total_amount = (

                    subtotal +

                    international_shipping

                )

            else:

                purchase.currency = "TZS"

                purchase.exchange_rate = 1

                purchase.total_amount = (

                    subtotal +

                    local_shipping

                )



            # =========================================
            # TZS EQUIVALENT
            # =========================================

            if purchase.currency == "USD":

                if purchase.exchange_rate <= 0:

                    purchase.exchange_rate = 1


                # ONLY USD PART IS CONVERTED

                usd_total = (

                    subtotal +

                    international_shipping

                )

                purchase.total_amount_tzs = (

                    usd_total *

                    purchase.exchange_rate

                ) + local_shipping

            else:

                purchase.currency = "TZS"

                purchase.exchange_rate = 1

                purchase.total_amount_tzs = (
                    purchase.total_amount
                )


            # =========================================
            # BALANCE
            # =========================================

            purchase.balance = (

                purchase.total_amount -

                purchase.amount_paid

            )


            # =========================================
            # PAYMENT STATUS
            # =========================================

            if purchase.total_amount <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"


            purchase.save()


            # =========================================
            # RESPONSE
            # =========================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Purchase updated successfully."
                    )

                }

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
# CREATE PURCHASE PAYMENT
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

            # =========================================
            # SAVE PAYMENT
            # =========================================

            payment = form.save(commit=False)

            payment.purchase = purchase

            payment.save()


            # =========================================
            # RECALCULATE TOTAL PAID
            # =========================================

            total_paid = (

                purchase.payments.aggregate(
                    total=Sum("amount")
                )["total"]

                or Decimal("0.00")

            )


            purchase.amount_paid = total_paid


            # =========================================
            # RECALCULATE BALANCE
            # =========================================

            purchase.balance = (

                purchase.total_amount -

                purchase.amount_paid

            )


            # =========================================
            # PAYMENT STATUS
            # =========================================

            if purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"


            purchase.save()


            # =========================================
            # RESPONSE
            # =========================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Purchase payment recorded "
                        "successfully."
                    )

                }

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
    
# =========================================
# ADDITIONAL COST LIST
# =========================================

def additional_cost_list(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    additional_costs = (
        purchase.additional_costs.all()
    )

    context = {

        "purchase": purchase,

        "additional_costs": additional_costs

    }

    return render(

        request,

        "purchases/additional_costs/list.html",

        context

    )
    
# =========================================
# CREATE ADDITIONAL COST
# =========================================

def additional_cost_create(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    form = PurchaseAdditionalCostForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            additional_cost = form.save(
                commit=False
            )

            additional_cost.purchase = purchase

            additional_cost.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Additional cost added successfully."
                    )

                }

            })

            return response

    context = {

        "form": form,

        "purchase": purchase

    }

    return render(
        request,
        "purchases/additional_costs/form.html",
        context
    )



# =========================================
# UPDATE ADDITIONAL COST
# =========================================

def additional_cost_update(request, pk):

    additional_cost = get_object_or_404(
        PurchaseAdditionalCost,
        pk=pk
    )

    form = PurchaseAdditionalCostForm(
        request.POST or None,
        instance=additional_cost
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "purchaseChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Additional cost updated successfully."
                    )

                }

            })

            return response

    context = {

        "form": form,

        "additional_cost": additional_cost

    }

    return render(
        request,
        "purchases/additional_costs/form.html",
        context
    )



# =========================================
# DELETE ADDITIONAL COST
# =========================================

def additional_cost_delete(request, pk):

    additional_cost = get_object_or_404(
        PurchaseAdditionalCost,
        pk=pk
    )

    if request.method == "POST":

        additional_cost.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps({

            "purchaseChanged": True,

            "closeModal": True

        })

        return response

    context = {
        "additional_cost": additional_cost
    }

    return render(
        request,
        "purchases/additional_costs/delete.html",
        context
    )
    
# =========================================
# ADDITIONAL COST LIST
# =========================================

def additional_cost_list(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    additional_costs = (
        purchase.additional_costs.all()
    )

    context = {

        "purchase": purchase,

        "additional_costs": additional_costs

    }

    return render(
        request,
        "purchases/additional_costs/list.html",
        context
    )



# =========================================
# ADDITIONAL COST TABLE
# =========================================

def additional_cost_table(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    additional_costs = (
        purchase.additional_costs.all()
    )

    context = {

        "purchase": purchase,

        "additional_costs": additional_costs

    }

    return render(
        request,
        "purchases/additional_costs/table.html",
        context
    )



# =========================================
# CREATE ADDITIONAL COST
# =========================================

def additional_cost_create(request, purchase_id):

    purchase = get_object_or_404(
        Purchase,
        pk=purchase_id
    )

    form = PurchaseAdditionalCostForm(
        request.POST or None
    )

    formset = AdditionalCostDocumentFormSet(

        request.POST or None,

        request.FILES or None,

        prefix="documents"

    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # =====================================
            # SAVE ADDITIONAL COST
            # =====================================

            additional_cost = form.save(
                commit=False
            )

            additional_cost.purchase = purchase

            additional_cost.save()

            # =====================================
            # SAVE DOCUMENTS
            # =====================================

            formset.instance = additional_cost

            formset.save()

            # =====================================
            # RESPONSE
            # =====================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "additionalCostChanged": {

                    "purchase_id": purchase.id

                },

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Additional cost added successfully."
                    )

                }

            })

            return response

    context = {

        "form": form,

        "formset": formset,

        "purchase": purchase

    }

    return render(
        request,
        "purchases/additional_costs/form.html",
        context
    )



# =========================================
# UPDATE ADDITIONAL COST
# =========================================

def additional_cost_update(request, pk):

    additional_cost = get_object_or_404(
        PurchaseAdditionalCost,
        pk=pk
    )

    form = PurchaseAdditionalCostForm(

        request.POST or None,

        instance=additional_cost

    )

    formset = AdditionalCostDocumentFormSet(

        request.POST or None,

        request.FILES or None,

        instance=additional_cost,

        prefix="documents"

    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # =====================================
            # SAVE COST
            # =====================================

            additional_cost = form.save()

            # =====================================
            # SAVE DOCUMENTS
            # =====================================

            formset.instance = additional_cost

            formset.save()

            # =====================================
            # RESPONSE
            # =====================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "additionalCostChanged": {

                    "purchase_id": (
                        additional_cost.purchase.id
                    )

                },

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Additional cost updated successfully."
                    )

                }

            })

            return response

    context = {

        "form": form,

        "formset": formset,

        "additional_cost": additional_cost

    }

    return render(
        request,
        "purchases/additional_costs/form.html",
        context
    )



# =========================================
# DELETE ADDITIONAL COST
# =========================================

def additional_cost_delete(request, pk):

    additional_cost = get_object_or_404(
        PurchaseAdditionalCost,
        pk=pk
    )

    if request.method == "POST":

        purchase_id = (
            additional_cost.purchase.id
        )

        additional_cost.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps({

            "additionalCostChanged": {

                "purchase_id": purchase_id

            },

            "closeModal": True,

            "showMessage": {

                "type": "success",

                "message": (
                    "Additional cost deleted successfully."
                )

            }

        })

        return response

    context = {
        "additional_cost": additional_cost
    }

    return render(
        request,
        "purchases/additional_costs/delete.html",
        context
    )