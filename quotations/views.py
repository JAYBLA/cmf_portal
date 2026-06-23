from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import QuotationForm, QuotationItemFormSet

from .models import *
from utils import render_to_pdf
from django.templatetags.static import static
from django.utils.text import slugify
import json


def quotation_list(request):

    quotations = Quotation.objects.select_related("customer").all()

    return render(request, "quotations/quotation_list.html", {"quotations": quotations})


# =========================================
# CREATE
# =========================================

def quotation_create(request):

    if request.method == "POST":

        form = QuotationForm(
            request.POST
        )

        if form.is_valid():

            quotation = form.save()

            formset = QuotationItemFormSet(
                request.POST,
                instance=quotation,
                prefix="items"
            )

            if formset.is_valid():

                formset.save()

                response = HttpResponse("")

                response["HX-Trigger"] = json.dumps({

                    "recordSaved": True,

                    "refreshTable": True,

                    "showMessage": {

                        "type": "success",

                        "message":
                            "Quotation created successfully."

                    }

                })

                return response

        else:

            formset = QuotationItemFormSet(
                request.POST,
                prefix="items"
            )

    else:

        form = QuotationForm()

        formset = QuotationItemFormSet(
            prefix="items"
        )

    return render(
        request,
        "quotations/partials/quotation_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )

# =========================================
# UPDATE
# =========================================

def quotation_update(request, pk):

    quotation = get_object_or_404(
        Quotation,
        pk=pk
    )

    if request.method == "POST":

        form = QuotationForm(
            request.POST,
            instance=quotation
        )

        formset = QuotationItemFormSet(
            request.POST,
            instance=quotation,
            prefix="items"
        )

        if form.is_valid() and formset.is_valid():

            form.save()

            formset.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Quotation updated successfully."

                }

            })

            return response

    else:

        form = QuotationForm(
            instance=quotation
        )

        formset = QuotationItemFormSet(
            instance=quotation,
            prefix="items"
        )

    return render(
        request,
        "quotations/partials/quotation_form.html",
        {
            "form": form,
            "formset": formset,
            "quotation": quotation,
        },
    )

# =========================================
# DELETE
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

            "recordSaved": True,

            "refreshTable": True,

            "showMessage": {

                "type": "success",

                "message":
                    "Quotation deleted successfully."

            }

        })

        return response

    return render(
        request,
        "quotations/partials/quotation_delete.html",
        {
            "quotation": quotation
        }
    )


# =========================================
# QUOTATION TABLE
# =========================================

def quotation_table(request):

    quotations = (
        Quotation.objects
        .select_related("customer")
        .all()
    )

    context = {
        "quotations": quotations
    }

    return render(
        request,
        "quotations/partials/quotation_table.html",
        context
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
        #below code is for pdf download
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        #below code is for pdf browser preview
        #response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response

    return HttpResponse("Error generating PDF", status=400)

def quotation_detail(request, pk):
    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "customer",
        ).prefetch_related(
            "items",
        ),
        pk=pk,
    )

    return render(
        request,
        "quotations/partials/quotation_detail.html",
        {
            "quotation": quotation,
        },
    )

