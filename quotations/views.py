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


def quotation_create(request):

    if request.method == "POST":

        form = QuotationForm(request.POST)

        if form.is_valid():

            quotation = form.save()

            formset = QuotationItemFormSet(
                request.POST, instance=quotation, prefix="items"
            )

            if formset.is_valid():

                formset.save()

                response = HttpResponse()

                response["HX-Refresh"] = "true"

                return response

        else:

            formset = QuotationItemFormSet(request.POST, prefix="items")

    else:

        form = QuotationForm()

        formset = QuotationItemFormSet(prefix="items")

    return render(
        request,
        "quotations/partials/quotation_form.html",
        {"form": form, "formset": formset},
    )


def quotation_update(request, pk):

    quotation = get_object_or_404(Quotation, pk=pk)

    if request.method == "POST":

        form = QuotationForm(request.POST, instance=quotation)

        formset = QuotationItemFormSet(request.POST, instance=quotation, prefix="items")

        if form.is_valid() and formset.is_valid():

            form.save()
            formset.save()

            response = HttpResponse()

            response["HX-Refresh"] = "true"

            return response

    else:

        form = QuotationForm(instance=quotation)

        formset = QuotationItemFormSet(instance=quotation, prefix="items")

    return render(
        request,
        "quotations/partials/quotation_form.html",
        {"form": form, "formset": formset, "quotation": quotation},
    )


def quotation_delete(request, pk):

    quotation = get_object_or_404(Quotation, pk=pk)

    if request.method == "POST":

        quotation.delete()

        response = HttpResponse()

        response["HX-Refresh"] = "true"

        return response

    return render(
        request, "quotations/partials/quotation_delete.html", {"quotation": quotation}
    )


def quotation_item_empty_row(request):

    total_forms = int(request.GET.get("total_forms", 0))

    formset = QuotationItemFormSet(prefix="items")

    form = formset.empty_form

    form.prefix = f"items-{total_forms}"

    return render(request, "quotations/partials/item_row.html", {"form": form})

# =====================================================
# DOWNLOAD
# =====================================================
def download_quotation_pdf(request, pk):

    quotation = get_object_or_404(Quotation, pk=pk)

    bg_image = request.build_absolute_uri(static("images/quotation.png"))

    context = {
        "quotation": quotation,
        "quotation_no": f"QT-{quotation.id}",
        "bg_image": bg_image,
    }

    pdf = render_to_pdf("quotations/quotation_pdf.html", context)

    if pdf:

        customer_name = slugify(quotation.customer.customer_name)

        quotation_title = slugify(quotation.title)

        filename = f"QT-{quotation.id}-" f"{customer_name}-" f"{quotation_title}.pdf"

        response = HttpResponse(pdf, content_type="application/pdf")

        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    return HttpResponse("Error generating PDF", status=400)