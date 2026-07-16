import json

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.templatetags.static import static
from django.utils.text import slugify

from utils import render_to_pdf

from .forms import ReceiptForm
from .models import Receipt

# =========================================
# RECEIPT LIST
# =========================================


def receipt_list(request):

    receipts = Receipt.objects.select_related(
        "invoice",
        "invoice__customer",
    ).all()

    context = {
        "receipts": receipts,
    }

    return render(
        request,
        "receipts/receipt_list.html",
        context,
    )


# =========================================
# RECEIPT TABLE
# =========================================


def receipt_table(request):

    receipts = Receipt.objects.select_related(
        "invoice",
        "invoice__customer",
    ).all()

    context = {
        "receipts": receipts,
    }

    return render(
        request,
        "receipts/partials/receipt_table.html",
        context,
    )


# =========================================
# CREATE RECEIPT
# =========================================


@transaction.atomic
def receipt_create(request):

    form = ReceiptForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST":

        if form.is_valid():

            # ---------------------------------
            # Save receipt
            # ---------------------------------

            receipt = form.save()

            # ---------------------------------
            # Update invoice payment status
            # ---------------------------------

            receipt.invoice.update_payment_status()

            # ---------------------------------
            # Response
            # ---------------------------------

            response = HttpResponse()

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Receipt created successfully."),
                    },
                }
            )

            return response

    context = {
        "form": form,
    }

    return render(
        request,
        "receipts/partials/receipt_form.html",
        context,
    )


# =========================================
# UPDATE RECEIPT
# =========================================


@transaction.atomic
def receipt_update(request, pk):

    receipt = get_object_or_404(
        Receipt.objects.select_related(
            "invoice",
        ),
        pk=pk,
    )

    # ---------------------------------
    # Store original invoice
    # ---------------------------------

    old_invoice = receipt.invoice
    old_payment_proof = receipt.payment_proof

    form = ReceiptForm(
        request.POST or None,
        request.FILES or None,
        instance=receipt,
    )

    if request.method == "POST":

        if form.is_valid():

            # ---------------------------------
            # Save receipt
            # ---------------------------------

            receipt = form.save()
            if (
                old_payment_proof
                and old_payment_proof != receipt.payment_proof
            ):
                old_payment_proof.delete(save=False)

            new_invoice = receipt.invoice

            # ---------------------------------
            # Update old invoice
            # ---------------------------------

            old_invoice.update_payment_status()

            # ---------------------------------
            # Update new invoice
            # ---------------------------------

            if old_invoice.pk != new_invoice.pk:

                new_invoice.update_payment_status()

            # ---------------------------------
            # Response
            # ---------------------------------

            response = HttpResponse()

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Receipt updated successfully."),
                    },
                }
            )

            return response

    context = {
        "receipt": receipt,
        "form": form,
    }

    return render(
        request,
        "receipts/partials/receipt_form.html",
        context,
    )


# =========================================
# DELETE RECEIPT
# =========================================


@transaction.atomic
def receipt_delete(request, pk):

    receipt = get_object_or_404(
        Receipt.objects.select_related(
            "invoice",
        ),
        pk=pk,
    )

    if request.method == "POST":

        # ---------------------------------
        # Store invoice before deletion
        # ---------------------------------

        invoice = receipt.invoice

        # ---------------------------------
        # Delete receipt
        # ---------------------------------
        if receipt.payment_proof:
            receipt.payment_proof.delete(save=False)
        receipt.delete()

        # ---------------------------------
        # Recalculate invoice
        # ---------------------------------

        invoice.update_payment_status()

        # ---------------------------------
        # Response
        # ---------------------------------

        response = HttpResponse()

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": ("Receipt deleted successfully."),
                },
            }
        )

        return response

    context = {
        "receipt": receipt,
    }

    return render(
        request,
        "receipts/partials/receipt_delete.html",
        context,
    )


# =========================================
# RECEIPT DETAIL
# =========================================


def receipt_detail(request, pk):

    receipt = get_object_or_404(
        Receipt.objects.select_related(
            "invoice",
            "invoice__customer",
        ),
        pk=pk,
    )

    context = {
        "receipt": receipt,
    }

    return render(
        request,
        "receipts/partials/receipt_detail.html",
        context,
    )


# =====================================================
# DOWNLOAD RECEIPT PDF
# =====================================================


def download_receipt_pdf(request, pk):

    receipt = get_object_or_404(
        Receipt.objects.select_related(
            "invoice",
            "invoice__customer",
        ),
        pk=pk,
    )

    # =========================================
    # BACKGROUND IMAGE
    # =========================================

    bg_image = request.build_absolute_uri(static("images/receipt.png"))

    # =========================================
    # CONTEXT
    # =========================================

    context = {
        "receipt": receipt,
        "receipt_no": receipt.receipt_number,
        "bg_image": bg_image,
    }

    # =========================================
    # GENERATE PDF
    # =========================================

    pdf = render_to_pdf(
        "receipts/receipt_pdf.html",
        context,
    )

    # =========================================
    # PDF RESPONSE
    # =========================================

    if pdf:

        customer_name = slugify(receipt.invoice.customer.customer_name)

        filename = f"{receipt.receipt_number}-" f"{customer_name}.pdf"

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )
        #Direct download
        
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    return HttpResponse(
        "Error generating receipt PDF",
        status=400,
    )
