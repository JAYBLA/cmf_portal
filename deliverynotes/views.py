import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.utils.text import slugify

from utils import render_to_pdf

from .forms import *
from .models import *
from quotations.models import Quotation


# =========================================
# DELIVERY NOTE LIST
# =========================================

def delivery_note_list(request):

    delivery_notes = (
        DeliveryNote.objects
        .select_related(
            "quotation",
            "quotation__customer",
        )
        .all()
    )

    return render(
        request,
        "delivery_notes/delivery_note_list.html",
        {
            "delivery_notes": delivery_notes,
        },
    )


# =========================================
# CREATE
# =========================================

def delivery_note_create(request):

    if request.method == "POST":

        form = DeliveryNoteForm(request.POST)

        if form.is_valid():

            delivery_note = form.save()

            quotation_items = request.POST.getlist("quotation_item")
            quantities = request.POST.getlist("quantity")
            remarks = request.POST.getlist("remarks")

            for quotation_item_id, quantity, remark in zip(
                quotation_items,
                quantities,
                remarks,
            ):

                if not quotation_item_id:
                    continue

                DeliveryNoteItem.objects.create(
                    delivery_note=delivery_note,
                    quotation_item_id=quotation_item_id,
                    quantity=quantity,
                    remarks=remark,
                )

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Delivery note created successfully.",
                    },
                }
            )

            return response

    else:

        form = DeliveryNoteForm()

    return render(
        request,
        "delivery_notes/partials/delivery_note_form.html",
        {
            "form": form,
        },
    )


# =========================================
# UPDATE
# =========================================

def delivery_note_update(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote,
        pk=pk,
    )

    if request.method == "POST":

        form = DeliveryNoteForm(
            request.POST,
            instance=delivery_note,
        )

        if form.is_valid():

            delivery_note = form.save()

            # Remove old rows
            delivery_note.items.all().delete()

            quotation_items = request.POST.getlist("quotation_item")
            quantities = request.POST.getlist("quantity")
            remarks = request.POST.getlist("remarks")

            for quotation_item_id, quantity, remark in zip(
                quotation_items,
                quantities,
                remarks,
            ):

                if not quotation_item_id:
                    continue

                DeliveryNoteItem.objects.create(
                    delivery_note=delivery_note,
                    quotation_item_id=quotation_item_id,
                    quantity=quantity,
                    remarks=remark,
                )

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Delivery note updated successfully.",
                    },
                }
            )

            return response

    else:

        form = DeliveryNoteForm(
            instance=delivery_note,
        )

    return render(
        request,
        "delivery_notes/partials/delivery_note_form.html",
        {
            "form": form,
            "delivery_note": delivery_note,
        },
    )

# =========================================
# DELETE
# =========================================

def delivery_note_delete(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote,
        pk=pk,
    )

    if request.method == "POST":

        delivery_note.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": "Delivery note deleted successfully.",
                },
            }
        )

        return response

    return render(
        request,
        "delivery_notes/partials/delivery_note_delete.html",
        {
            "delivery_note": delivery_note,
        },
    )


# =========================================
# DELIVERY NOTE TABLE
# =========================================

def delivery_note_table(request):

    delivery_notes = (
        DeliveryNote.objects
        .select_related(
            "quotation",
            "quotation__customer",
        )
        .all()
    )

    return render(
        request,
        "delivery_notes/partials/delivery_note_table.html",
        {
            "delivery_notes": delivery_notes,
        },
    )


# =====================================================
# DOWNLOAD
# =====================================================

def download_delivery_note_pdf(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote,
        pk=pk,
    )

    bg_image = request.build_absolute_uri(
        static("images/delivery_note.png")
    )

    context = {
        "delivery_note": delivery_note,
        "delivery_number": delivery_note.delivery_number,
        "bg_image": bg_image,
    }

    pdf = render_to_pdf(
        "delivery_notes/delivery_note_pdf.html",
        context,
    )

    if pdf:

        customer_name = slugify(
            delivery_note.customer.customer_name
        )

        filename = (
            f"{delivery_note.delivery_number}-"
            f"{customer_name}.pdf"
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{filename}"'
        )

        return response

    return HttpResponse(
        "Error generating PDF",
        status=400,
    )


# =========================================
# DETAIL
# =========================================

def delivery_note_detail(request, pk):

    delivery_note = get_object_or_404(
        DeliveryNote.objects
        .select_related(
            "quotation",
            "quotation__customer",
        )
        .prefetch_related(
            "items",
            "items__quotation_item",
        ),
        pk=pk,
    )

    return render(
        request,
        "delivery_notes/partials/delivery_note_detail.html",
        {
            "delivery_note": delivery_note,
        },
    )
    
def quotation_items(request, quotation_id):

    quotation = get_object_or_404(
        Quotation.objects.prefetch_related("items"),
        pk=quotation_id,
    )

    return render(
        request,
        "delivery_notes/partials/quotation_items_rows.html",
        {
            "quotation": quotation,
        },
    )