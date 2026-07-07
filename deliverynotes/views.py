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
from utils import (
    apply_document_backgrounds,
)
from django.template.loader import render_to_string
from django.utils.text import slugify

from weasyprint import HTML
from pathlib import Path

from django.contrib.staticfiles import finders


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
    
# =====================================================
# DOWNLOAD DELIVERYNOTE PDF
# =====================================================


def download_delivery_note_pdf(request, pk):

    # =========================================
    # GET DELIVERYNOTE
    # =========================================

    delivery_note = get_object_or_404(
        DeliveryNote.objects.select_related(
            "quotation",
            "quotation__customer",
        ).prefetch_related(
            "items",
            "items__quotation_item",
            "items__quotation_item__product",
        ),
        pk=pk,
    )


    # =========================================
    # BACKGROUND IMAGE PATHS
    # =========================================

    header_path = finders.find(
        "images/delivery_note_header.png"
    )


    footer_path = finders.find(
        "images/delivery_note_footer.png"
    )


    single_path = finders.find(
        "images/delivery_note_single.png"
    )

    # =========================================
    # VALIDATE BACKGROUND FILES
    # =========================================

    if not header_path:

        raise FileNotFoundError(
            "quote_header.png was not found."
        )


    if not footer_path:

        raise FileNotFoundError(
            "quote_footer.png was not found."
        )


    if not single_path:

        raise FileNotFoundError(
            "quotation_single.png was not found."
        )


    # =========================================
    # FILE URIS
    # =========================================

    header_bg = Path(
        header_path
    ).resolve().as_uri()


    footer_bg = Path(
        footer_path
    ).resolve().as_uri()


    single_bg = Path(
        single_path
    ).resolve().as_uri()

    # =========================================
    # FONT
    # =========================================

    poppins_font_path = finders.find(
        "fonts/Poppins-Regular.ttf"
    )


    if poppins_font_path:

        poppins_font = (
            Path(poppins_font_path)
            .resolve()
            .as_uri()
        )

    else:

        poppins_font = None

    # =========================================
    # BASE CONTEXT
    # =========================================

    context_data = {

        "delivery_note": delivery_note,

        "customer": delivery_note.customer,

        "quotation": delivery_note.quotation,
        "poppins_font": poppins_font,

    }


    # =========================================
    # FIRST PAGINATION PASS
    # =========================================

    page_count = 1


    for _ in range(5):

        context = {

            **context_data,

            "page_count": page_count,

        }


        html = render_to_string(
            "delivery_notes/delivery_note_pdf.html",
            context,
            request=request,
        )


        document = HTML(
            string=html,
        ).render()


        actual_page_count = len(
            document.pages
        )


        # =====================================
        # PAGINATION IS STABLE
        # =====================================

        if actual_page_count == page_count:

            break


        # =====================================
        # UPDATE PAGE COUNT
        # =====================================

        page_count = actual_page_count


    # =========================================
    # FINAL HTML CONTEXT
    # =========================================

    final_context = {

        **context_data,

        "page_count": page_count,

    }


    # =========================================
    # FINAL HTML
    # =========================================

    final_html = render_to_string(
        "delivery_notes/delivery_note_pdf.html",
        final_context,
        request=request,
    )


    # =========================================
    # GENERATE CONTENT PDF
    # =========================================

    content_pdf = HTML(
        string=final_html,
    ).write_pdf()


    # =========================================
    # APPLY PAGE BACKGROUNDS
    # =========================================

    pdf = apply_document_backgrounds(
        content_pdf=content_pdf,
        header_bg=header_bg,
        footer_bg=footer_bg,
        single_bg=single_bg,
    )


    # =========================================
    # CUSTOMER NAME
    # =========================================

    customer_name = slugify(
        delivery_note.customer.customer_name
    )


    # =========================================
    # DELIVERY NUMBER
    # =========================================

    delivery_number = slugify(
        delivery_note.delivery_number
    )


    # =========================================
    # FILE NAME
    # =========================================

    filename = (

        f"{delivery_number}-"

        f"{customer_name}.pdf"

    )


    # =========================================
    # PDF RESPONSE
    # =========================================

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )


    response["Content-Disposition"] = (

        "attachment; "

        f'filename="{filename}"'

    )


    return response