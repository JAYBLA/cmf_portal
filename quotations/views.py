import json
from decimal import Decimal

from django.http import (
    HttpResponse,
)

from django.shortcuts import (
    render,
    get_object_or_404,
)

from .models import (
    Quotation,
)

from .forms import (
    QuotationForm,
    QuotationItemFormSet,
)
from utils import render_to_pdf
from django.templatetags.static import static
from django.utils.text import slugify
import json

# =========================================
# QUOTATION LIST
# =========================================


def quotation_list(request):

    quotations = Quotation.objects.select_related(
        "customer",        
    ).prefetch_related("items")

    context = {
        "quotations": quotations,
    }

    return render(
        request,
        "quotations/quotation_list.html",
        context,
    )


# =========================================
# QUOTATION TABLE
# =========================================


def quotation_table(request):

    quotations = Quotation.objects.select_related(
        "customer",       
    ).prefetch_related("items")

    context = {
        "quotations": quotations,
    }

    return render(
        request,
        "quotations/partials/quotation_table.html",
        context,
    )


# =========================================
# CREATE QUOTATION
# =========================================


# =========================================
# CREATE QUOTATION
# =========================================

def quotation_create(request):

    form = QuotationForm(request.POST or None)

    formset = QuotationItemFormSet(
        request.POST or None,
        prefix="items",
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # ---------------------------------
            # Save quotation
            # ---------------------------------

            quotation = form.save(commit=False)

            quotation.save()

            form.save_m2m()

            # ---------------------------------
            # Save items
            # ---------------------------------

            formset.instance = quotation

            items = formset.save(commit=False)

            for item in items:

                item.quotation = quotation

                item.save()

            # ---------------------------------
            # Delete removed items
            # ---------------------------------

            for obj in formset.deleted_objects:

                obj.delete()

            formset.save_m2m()

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
                        "message": "Quotation created successfully.",
                    },
                }
            )

            return response

    context = {
        "form": form,
        "formset": formset,
    }

    return render(
        request,
        "quotations/partials/quotation_form.html",
        context,
    )

# =========================================
# UPDATE QUOTATION
# =========================================


# =========================================
# UPDATE QUOTATION
# =========================================

def quotation_update(request, pk):

    quotation = get_object_or_404(
        Quotation,
        pk=pk,
    )

    form = QuotationForm(
        request.POST or None,
        instance=quotation,
    )

    formset = QuotationItemFormSet(
        request.POST or None,
        instance=quotation,
        prefix="items",
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # ---------------------------------
            # Save quotation
            # ---------------------------------

            quotation = form.save(commit=False)

            quotation.save()

            form.save_m2m()

            # ---------------------------------
            # Save items
            # ---------------------------------

            formset.instance = quotation

            items = formset.save(commit=False)

            for item in items:

                item.quotation = quotation

                item.save()

            # ---------------------------------
            # Delete removed items
            # ---------------------------------

            for obj in formset.deleted_objects:

                obj.delete()

            formset.save_m2m()

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
                        "message": "Quotation updated successfully.",
                    },
                }
            )

            return response

    context = {
        "quotation": quotation,
        "form": form,
        "formset": formset,
    }

    return render(
        request,
        "quotations/partials/quotation_form.html",
        context,
    )


# =========================================
# DELETE QUOTATION
# =========================================


def quotation_delete(request, pk):

    quotation = get_object_or_404(
        Quotation,
        pk=pk,
    )

    if request.method == "POST":

        quotation.delete()

        response = HttpResponse()

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": "Quotation deleted successfully.",
                },
            }
        )

        return response

    context = {
        "quotation": quotation,
    }

    return render(
        request,
        "quotations/partials/quotation_delete.html",
        context,
    )


# =========================================
# QUOTATION DETAIL
# =========================================


def quotation_detail(request, pk):

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "customer",
            "payment_terms",
        ).prefetch_related(
            "items",
        ),
        pk=pk,
    )

    context = {
        "quotation": quotation,
    }

    return render(
        request,
        "quotations/partials/quotation_detail.html",
        context,
    )


# =====================================================
# DOWNLOAD
# =====================================================
def download_quotation_pdf(request, pk):

    quotation = get_object_or_404(Quotation, pk=pk)

    bg_image = request.build_absolute_uri(static("images/quotation.png"))

    context = {
        "quotation": quotation,
        "quotation_no": f"CMFQ00{quotation.id}",
        "bg_image": bg_image,
    }

    pdf = render_to_pdf("quotations/quotation_pdf.html", context)

    if pdf:

        customer_name = slugify(quotation.customer.customer_name)

        quotation_title = slugify(quotation.title)

        filename = f"CMFQ00{quotation.id}-" f"{customer_name}-" f"{quotation_title}.pdf"

        response = HttpResponse(pdf, content_type="application/pdf")
        # below code is for pdf download
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        # below code is for pdf browser preview
        #response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response

    return HttpResponse("Error generating PDF", status=400)
