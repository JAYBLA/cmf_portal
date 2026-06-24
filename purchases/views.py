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
from .services.pricing import recalculate_purchase_pricing

# =========================================
# PURCHASE LIST
# =========================================


def purchase_list(request):

    purchases = Purchase.objects.select_related("supplier").all()

    context = {"purchases": purchases}

    return render(request, "purchases/purchase_list.html", context)


# =========================================
# PURCHASE TABLE PARTIAL
# =========================================


def purchase_table(request):

    purchases = Purchase.objects.select_related("supplier").all()

    context = {"purchases": purchases}

    return render(request, "purchases/partials/purchase_table.html", context)


# =========================================
# CREATE PURCHASE
# =========================================


def purchase_create(request):

    form = PurchaseForm(request.POST or None)

    formset = PurchaseItemFormSet(request.POST or None, prefix="items")

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # =====================================
            # CREATE PURCHASE
            # =====================================

            purchase = form.save(commit=False)

            purchase.subtotal = Decimal("0.00")
            purchase.total_amount = Decimal("0.00")
            purchase.total_amount_tzs = Decimal("0.00")
            purchase.balance = Decimal("0.00")

            purchase.save()

            # =====================================
            # SAVE ITEMS
            # =====================================

            formset.instance = purchase

            items = formset.save(commit=False)

            for item in items:

                item.purchase = purchase

                item.save()

                item.product.update_stock(
                    quantity=item.quantity,
                    movement_type="in",
                    reference=purchase.purchase_number,
                    notes="Purchase Stock In",
                )

            # =====================================
            # DELETE MARKED ITEMS
            # =====================================

            for obj in formset.deleted_objects:

                obj.delete()

            # =====================================
            # CALCULATE TOTALS
            # =====================================

            subtotal = Decimal("0.00")

            for item in purchase.items.all():

                subtotal += item.subtotal

            purchase.subtotal = subtotal

            if purchase.currency == "USD":

                purchase.total_amount = subtotal

                purchase.total_amount_tzs = subtotal * purchase.exchange_rate

            else:

                purchase.total_amount = subtotal

                purchase.total_amount_tzs = subtotal

            purchase.balance = purchase.total_amount - purchase.amount_paid

            purchase.save()
            recalculate_purchase_pricing(purchase)

            # =====================================
            # RESPONSE
            # =====================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Purchase saved successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "products": Product.objects.filter(status="active"),
    }

    return render(request, "purchases/partials/purchase_form.html", context)


# =========================================
# UPDATE PURCHASE
# =========================================


def purchase_update(request, pk):

    purchase = get_object_or_404(Purchase, pk=pk)

    form = PurchaseForm(request.POST or None, instance=purchase)

    formset = PurchaseItemFormSet(
        request.POST or None, instance=purchase, prefix="items"
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # =====================================
            # REVERSE EXISTING STOCK
            # =====================================

            for old_item in purchase.items.all():

                old_item.product.update_stock(
                    quantity=old_item.quantity,
                    movement_type="out",
                    reference=purchase.purchase_number,
                    notes="Purchase Update Reversal",
                )

            # =====================================
            # SAVE PURCHASE
            # =====================================

            purchase = form.save(commit=False)

            purchase.save()

            # =====================================
            # SAVE ITEMS
            # =====================================

            formset.instance = purchase

            items = formset.save(commit=False)

            for obj in formset.deleted_objects:

                obj.delete()

            for item in items:

                item.purchase = purchase

                item.save()

                item.product.update_stock(
                    quantity=item.quantity,
                    movement_type="in",
                    reference=purchase.purchase_number,
                    notes="Purchase Update",
                )

            # =====================================
            # RECALCULATE TOTALS
            # =====================================

            subtotal = Decimal("0.00")

            for item in purchase.items.all():

                subtotal += item.subtotal

            purchase.subtotal = subtotal

            if purchase.currency == "USD":

                purchase.total_amount = subtotal

                purchase.total_amount_tzs = subtotal * purchase.exchange_rate

            else:

                purchase.total_amount = subtotal

                purchase.total_amount_tzs = subtotal

            purchase.balance = purchase.total_amount - purchase.amount_paid

            if purchase.amount_paid <= 0:

                purchase.payment_status = "pending"

            elif purchase.amount_paid < purchase.total_amount:

                purchase.payment_status = "partial"

            else:

                purchase.payment_status = "paid"

            purchase.save()
            recalculate_purchase_pricing(purchase)

            # =====================================
            # RESPONSE
            # =====================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Purchase updated successfully.",
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "purchase": purchase,
        "products": Product.objects.filter(status="active"),
    }

    return render(request, "purchases/partials/purchase_form.html", context)


# =========================================
# DELETE PURCHASE
# =========================================


def purchase_delete(request, pk):

    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == "POST":

        # =====================================
        # REVERSE STOCK
        # =====================================

        for item in purchase.items.all():

            item.product.update_stock(
                quantity=item.quantity,
                movement_type="out",
                reference=purchase.purchase_number,
                notes="Purchase Deleted",
            )

        # =====================================
        # DELETE PURCHASE
        # =====================================

        purchase.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": "Purchase deleted successfully.",
                },
            }
        )

        return response

    context = {"purchase": purchase}

    return render(request, "purchases/partials/purchase_delete.html", context)


# =========================================
# CREATE PURCHASE PAYMENT
# =========================================


def purchase_payment_create(request, purchase_id):

    purchase = get_object_or_404(Purchase, pk=purchase_id)

    form = PurchasePaymentForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            # =====================================
            # SAVE PAYMENT
            # =====================================

            payment = form.save(commit=False)

            payment.purchase = purchase

            payment.save()

            # =====================================
            # RESPONSE
            # =====================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Purchase payment " "recorded successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
        "purchase": purchase,
    }

    return render(request, "purchases/payments/payment_form.html", context)


# =========================================
# ADDITIONAL COST LIST
# =========================================


def additional_cost_list(request, purchase_id):

    purchase = get_object_or_404(Purchase, pk=purchase_id)

    additional_costs = purchase.additional_costs.select_related(
        "clearing_agent"
    ).order_by("id")

    context = {
        "purchase": purchase,
        "additional_costs": additional_costs,
    }

    return render(request, "purchases/additional_costs/list.html", context)


# =========================================
# CREATE ADDITIONAL COST
# =========================================


def additional_cost_create(request, purchase_id):

    purchase = get_object_or_404(Purchase, pk=purchase_id)

    form = PurchaseAdditionalCostForm(request.POST or None)

    formset = AdditionalCostDocumentFormSet(
        request.POST or None,
        request.FILES or None,
        prefix="documents",
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            additional_cost = form.save(commit=False)

            additional_cost.purchase = purchase

            additional_cost.save()

            formset.instance = additional_cost

            formset.save()
            recalculate_purchase_pricing(purchase)

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Additional cost added successfully.",
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "purchase": purchase,
    }

    return render(request, "purchases/additional_costs/form.html", context)


# =========================================
# UPDATE ADDITIONAL COST
# =========================================


def additional_cost_update(request, pk):

    additional_cost = get_object_or_404(PurchaseAdditionalCost, pk=pk)

    form = PurchaseAdditionalCostForm(request.POST or None, instance=additional_cost)

    formset = AdditionalCostDocumentFormSet(
        request.POST or None,
        request.FILES or None,
        instance=additional_cost,
        prefix="documents",
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            additional_cost = form.save()

            formset.instance = additional_cost

            formset.save()
            recalculate_purchase_pricing(additional_cost.purchase)

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Additional cost updated successfully.",
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
        "additional_cost": additional_cost,
        "purchase": additional_cost.purchase,
    }

    return render(request, "purchases/additional_costs/form.html", context)


# =========================================
# DELETE ADDITIONAL COST
# =========================================


def additional_cost_delete(request, pk):

    additional_cost = get_object_or_404(PurchaseAdditionalCost, pk=pk)
    purchase = additional_cost.purchase

    if request.method == "POST":

        try:

            additional_cost.delete()
            recalculate_purchase_pricing(purchase)

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Additional cost deleted successfully.",
                    },
                }
            )

            return response

        except Exception as e:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "showMessage": {
                        "type": "error",
                        "message": f"Unable to delete additional cost. {str(e)}",
                    }
                }
            )

            return response

    context = {
        "additional_cost": additional_cost,
    }

    return render(request, "purchases/additional_costs/delete.html", context)


# =========================================
# ADDITIONAL COST TABLE
# =========================================


def additional_cost_table(request, purchase_id):

    purchase = get_object_or_404(Purchase, pk=purchase_id)

    additional_costs = purchase.additional_costs.select_related(
        "clearing_agent"
    ).order_by("id")

    context = {
        "purchase": purchase,
        "additional_costs": additional_costs,
    }

    return render(request, "purchases/additional_costs/table.html", context)

# =========================================
# ADDITIONAL COST DOCUMENTS
# =========================================

def additional_cost_documents(request, pk):

    additional_cost = get_object_or_404(
        PurchaseAdditionalCost,
        pk=pk
    )

    documents = additional_cost.documents.all()

    context = {
        "additional_cost": additional_cost,
        "documents": documents,
    }

    return render(
        request,
        "purchases/additional_costs/documents.html",
        context,
    )