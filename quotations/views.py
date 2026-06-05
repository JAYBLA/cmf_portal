import json

from decimal import Decimal

from django.shortcuts import (
    render,
    get_object_or_404
)

from django.http import HttpResponse, JsonResponse

from .models import *

from .forms import *
from products.models import *


# =========================================
# QUOTATION LIST
# =========================================

def quotation_list(request):

    quotations = (
        Quotation.objects
        .select_related("customer")
    )

    context = {
        "quotations": quotations
    }

    return render(
        request,
        "quotations/list.html",
        context
    )


# =========================================
# QUOTATION TABLE
# =========================================

def quotation_table(request):

    quotations = (
        Quotation.objects
        .select_related("customer")
    )

    context = {
        "quotations": quotations
    }

    return render(
        request,
        "quotations/table.html",
        context
    )


# =========================================
# CREATE QUOTATION
# =========================================

def quotation_create(request):

    form = QuotationForm(
        request.POST or None
    )

    formset = QuotationItemFormSet(
        request.POST or None,
        prefix="items"
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            quotation = form.save(
                commit=False
            )

            quotation.subtotal = Decimal("0.00")

            quotation.total_amount = Decimal("0.00")

            quotation.save()

            formset.instance = quotation

            items = formset.save(
                commit=False
            )

            subtotal = Decimal("0.00")

            for item in items:

                item.quotation = quotation

                item.save()

                subtotal += item.subtotal

            for obj in formset.deleted_objects:

                obj.delete()

            quotation.subtotal = subtotal

            quotation.total_amount = max(

                Decimal("0.00"),

                subtotal -

                quotation.discount_amount

            )

            quotation.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "quotationChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Quotation created successfully."
                    )

                }

            })

            return response

    context = {

        "form": form,

        "formset": formset

    }

    return render(

        request,

        "quotations/form.html",

        context

    )


# =========================================
# UPDATE QUOTATION
# =========================================

def quotation_update(request, pk):

    quotation = get_object_or_404(

        Quotation,

        pk=pk

    )

    form = QuotationForm(

        request.POST or None,

        instance=quotation

    )

    formset = QuotationItemFormSet(

        request.POST or None,

        instance=quotation,

        prefix="items"

    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            quotation = form.save()

            items = formset.save(
                commit=False
            )

            for item in items:

                item.quotation = quotation

                item.save()

            for obj in formset.deleted_objects:

                obj.delete()

            subtotal = Decimal("0.00")

            for item in quotation.items.all():

                subtotal += item.subtotal

            quotation.subtotal = subtotal

            quotation.total_amount = max(

                Decimal("0.00"),

                subtotal -

                quotation.discount_amount

            )

            quotation.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "quotationChanged": True,

                "closeModal": True,

                "showMessage": {

                    "type": "success",

                    "message": (
                        "Quotation updated successfully."
                    )

                }

            })

            return response

    context = {

        "quotation": quotation,

        "form": form,

        "formset": formset

    }

    return render(

        request,

        "quotations/form.html",

        context

    )


# =========================================
# DELETE QUOTATION
# =========================================

def quotation_delete(request, pk):

    quotation = get_object_or_404(
        Quotation,
        pk=pk
    )

    if request.method == "POST":

        quotation.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps({

            "quotationChanged": True,

            "closeModal": True,

            "showMessage": {

                "type": "success",

                "message": (
                    "Quotation deleted successfully."
                )

            }

        })

        return response

    context = {
        "quotation": quotation
    }

    return render(
        request,
        "quotations/delete.html",
        context
    )
    
# =========================================
# PRODUCT DETAILS
# =========================================

def quotation_product_details(request):

    product_id = request.GET.get(
        "product_id"
    )

    if not product_id:

        return JsonResponse({})

    product = get_object_or_404(

        Product,

        pk=product_id

    )

    return JsonResponse({

        "description":
            product.product_name,

        "unit_price":
            float(
                product.selling_price
            )

    })