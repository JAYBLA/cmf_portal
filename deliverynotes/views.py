import json

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    render,
)

from quotations.models import Quotation

from .forms import *

from .models import *
from decimal import Decimal

from django.db.models import Sum


# =========================================
# DELIVERYNOTE LIST
# =========================================


def delivery_note_list(request):

    delivery_notes = (
        DeliveryNote.objects
        .select_related(
            "quotation",
            "quotation__customer",
        )
        .prefetch_related(
            "items",
            "items__quotation_item",
        )
    )


    context = {
        "delivery_notes": delivery_notes,
    }


    return render(
        request,
        "delivery_notes/delivery_note_list.html",
        context,
    )


# =========================================
# DELIVERYNOTE TABLE
# =========================================


def delivery_note_table(request):

    delivery_notes = (
        DeliveryNote.objects
        .select_related(
            "quotation",
            "quotation__customer",
        )
        .prefetch_related(
            "items",
            "items__quotation_item",
        )
    )


    context = {
        "delivery_notes": delivery_notes,
    }


    return render(
        request,
        "delivery_notes/partials/delivery_note_table.html",
        context,
    )


# =========================================
# CREATE DELIVERYNOTE
# =========================================


@transaction.atomic
def delivery_note_create(request):

    form = DeliveryNoteForm(
        request.POST or None
    )


    if request.method == "POST":

        formset = DeliveryNoteItemFormSet(
            request.POST,
            prefix="items",
        )


        if (
            form.is_valid()
            and formset.is_valid()
        ):

            delivery_note = form.save()


            formset.instance = delivery_note


            items = formset.save(
                commit=False
            )


            for item in items:

                item.delivery_note = (
                    delivery_note
                )

                item.save()


            for obj in formset.deleted_objects:

                obj.delete()


            delivery_note.update_delivery_status()


            response = HttpResponse()


            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,

                    "refreshTable": True,

                    "showMessage": {
                        "type": "success",

                        "message": (
                            "Delivery note created "
                            "successfully."
                        ),
                    },
                }
            )


            return response


    else:

        formset = DeliveryNoteItemFormSet(
            prefix="items",
        )


    context = {
        "form": form,
        "formset": formset,
    }


    return render(
        request,
        "delivery_notes/partials/delivery_note_form.html",
        context,
    )


# =========================================
# UPDATE DELIVERYNOTE
# =========================================


@transaction.atomic
def delivery_note_update(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote,
        pk=pk,
    )


    form = DeliveryNoteForm(
        request.POST or None,
        instance=delivery_note,
    )


    formset = DeliveryNoteItemFormSet(
        request.POST or None,
        instance=delivery_note,
        prefix="items",
    )


    if request.method == "POST":

        if (
            form.is_valid()
            and formset.is_valid()
        ):

            delivery_note = form.save()


            formset.instance = delivery_note


            items = formset.save(
                commit=False
            )


            for item in items:

                item.delivery_note = (
                    delivery_note
                )

                item.save()


            for obj in formset.deleted_objects:

                obj.delete()


            delivery_note.update_delivery_status()


            response = HttpResponse()


            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,

                    "refreshTable": True,

                    "showMessage": {
                        "type": "success",

                        "message": (
                            "Delivery note updated "
                            "successfully."
                        ),
                    },
                }
            )


            return response


    context = {
        "delivery_note": delivery_note,
        "form": form,
        "formset": formset,
    }


    return render(
        request,
        "delivery_notes/partials/delivery_note_form.html",
        context,
    )

# =========================================
# QUOTATION ITEMS
# =========================================


def quotation_items(request, quotation_id):

    quotation = get_object_or_404(
        Quotation.objects.prefetch_related(
            "items",
        ),
        pk=quotation_id,
    )


    initial = []


    # =========================================
    # BUILD REMAINING DELIVERY ITEMS
    # =========================================

    for quotation_item in quotation.items.all():

        delivered_quantity = (
            quotation_item
            .delivery_items
            .aggregate(
                total=Sum("quantity")
            )["total"]
            or Decimal("0")
        )


        remaining_quantity = (
            quotation_item.quantity
            - delivered_quantity
        )


        if remaining_quantity <= 0:
            continue


        initial.append(
            {
                "quotation_item":
                    quotation_item.pk,

                "quantity":
                    remaining_quantity,

                "remarks":
                    "",
            }
        )


    # =========================================
    # DYNAMIC FORMSET
    # =========================================

    QuotationDeliveryItemFormSet = (
        inlineformset_factory(
            parent_model=DeliveryNote,
            model=DeliveryNoteItem,
            form=DeliveryNoteItemForm,
            extra=len(initial),
            can_delete=True,
        )
    )


    formset = QuotationDeliveryItemFormSet(
        initial=initial,
        prefix="items",
    )


    context = {
        "quotation": quotation,
        "formset": formset,
    }


    return render(
        request,
        (
            "delivery_notes/partials/"
            "quotation_items_rows.html"
        ),
        context,
    )
    
# =========================================
# DELIVERY NOTE DETAIL
# =========================================


def delivery_note_detail(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote.objects.select_related(
            "quotation",
            "quotation__customer",
        ).prefetch_related(
            "items",
            "items__quotation_item",
        ),
        pk=pk,
    )


    context = {
        "delivery_note": delivery_note,
    }


    return render(
        request,
        (
            "delivery_notes/partials/"
            "delivery_note_detail.html"
        ),
        context,
    )
    
# =========================================
# DELETE DELIVERY NOTE
# =========================================


def delivery_note_delete(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote,
        pk=pk,
    )

    if request.method == "POST":

        delivery_number = (
            delivery_note.delivery_number
        )

        delivery_note.delete()

        response = HttpResponse()

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": (
                        f"Delivery note "
                        f"{delivery_number} "
                        f"deleted successfully."
                    ),
                },
            }
        )

        return response

    context = {
        "delivery_note": delivery_note,
    }

    return render(
        request,
        (
            "delivery_notes/partials/"
            "delivery_note_delete.html"
        ),
        context,
    )