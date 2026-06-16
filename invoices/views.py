from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import InvoiceForm, InvoiceItemFormSet
from .models import *

from utils import render_to_pdf
from django.templatetags.static import static
from django.utils.text import slugify
from django.db import transaction

from customers.models import *
from products.models import *

# =====================================================
# HELPER
# =====================================================


def update_invoice_totals(invoice):

    subtotal = sum(item.subtotal for item in invoice.items.all())

    invoice.subtotal = subtotal

    invoice.total_amount = subtotal - invoice.discount_amount

    invoice.balance = invoice.total_amount - invoice.amount_paid

    if invoice.balance <= 0 and invoice.total_amount > 0:

        invoice.status = "paid"

    elif invoice.amount_paid > 0:

        invoice.status = "partial"

    elif invoice.total_amount > 0:

        invoice.status = "unpaid"

    invoice.save()


# =====================================================
# LIST
# =====================================================


def invoice_list(request):

    invoices = Invoice.objects.select_related("customer").all()

    return render(
        request,
        "invoices/invoice_list.html",
        {"invoices": invoices},
    )

# =====================================================
# CREATE
# =====================================================
@transaction.atomic
def invoice_create(request):

    if request.method == "POST":

        form = InvoiceForm(request.POST)

        formset = InvoiceItemFormSet(
            request.POST,
            prefix="items",
        )

        if form.is_valid() and formset.is_valid():

            invoice = form.save(commit=False)

            # ==================================
            # CUSTOMER
            # ==================================

            customer_value = (
                form.cleaned_data["customer_text"]
                .strip()
            )

            try:

                customer = Customer.objects.get(
                    pk=int(customer_value)
                )

            except (
                ValueError,
                TypeError,
                Customer.DoesNotExist,
            ):

                customer, _ = Customer.objects.get_or_create(
                    customer_name=customer_value
                )

            invoice.customer = customer

            invoice.save()

            # ==================================
            # ITEMS
            # ==================================

            for item_form in formset.forms:

                if not item_form.cleaned_data:
                    continue

                if item_form.cleaned_data.get("DELETE"):
                    continue

                product = item_form.cleaned_data.get(
                    "product"
                )

                description = item_form.cleaned_data.get(
                    "description"
                )

                quantity = item_form.cleaned_data.get(
                    "quantity"
                )

                unit_price = item_form.cleaned_data.get(
                    "unit_price"
                )

                if (
                    quantity is None
                    or unit_price is None
                ):
                    continue

                # Require either product or description

                if not product and not description:
                    continue

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                )

            update_invoice_totals(invoice)

            response = HttpResponse()

            response["HX-Refresh"] = "true"

            return response

    else:

        form = InvoiceForm()       
        formset = InvoiceItemFormSet(
            prefix="items"
        )

    return render(
        request,
        "invoices/partials/invoice_form.html",
        {
            "form": form,
            "formset": formset,           
        },
    )


    
@transaction.atomic
def invoice_update(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
    )

    if request.method == "POST":

        form = InvoiceForm(
            request.POST,
            instance=invoice,
        )

        formset = InvoiceItemFormSet(
            request.POST,
            instance=invoice,
            prefix="items",
        )

        if form.is_valid() and formset.is_valid():

            invoice = form.save(commit=False)

            # ==================================
            # CUSTOMER
            # ==================================

            customer_value = (
                form.cleaned_data["customer_text"]
                .strip()
            )

            try:

                customer = Customer.objects.get(
                    pk=int(customer_value)
                )

            except (
                ValueError,
                TypeError,
                Customer.DoesNotExist,
            ):

                customer, _ = Customer.objects.get_or_create(
                    customer_name=customer_value
                )

            invoice.customer = customer

            invoice.save()

            # ==================================
            # ITEMS
            # ==================================

            for item_form in formset.forms:

                if not item_form.cleaned_data:
                    continue

                item = item_form.save(commit=False)

                if item_form.cleaned_data.get("DELETE"):

                    if item.pk:
                        item.delete()

                    continue

                if (
                    not item.product
                    and not item.description
                ):
                    continue

                item.invoice = invoice

                item.save()

            update_invoice_totals(invoice)

            response = HttpResponse()

            response["HX-Refresh"] = "true"

            return response

    else:

        form = InvoiceForm(
            instance=invoice,
        )

        formset = InvoiceItemFormSet(
            instance=invoice,
            prefix="items",
        )

    return render(
        request,
        "invoices/partials/invoice_form.html",
        {
            "form": form,
            "formset": formset,
            "invoice": invoice,
        },
    )

# =====================================================
# DELETE
# =====================================================


def invoice_delete(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
    )

    if request.method == "POST":

        invoice.delete()

        response = HttpResponse()

        response["HX-Refresh"] = "true"

        return response

    return render(
        request,
        "invoices/partials/invoice_delete.html",
        {"invoice": invoice},
    )


# =====================================================
# EMPTY ITEM ROW
# =====================================================


def invoice_item_empty_row(request):

    total_forms = int(request.GET.get("total_forms", 0))

    formset = InvoiceItemFormSet(prefix="items")

    form = formset.empty_form

    form.prefix = f"items-{total_forms}"

    return render(
        request,
        "invoices/partials/item_row.html",
        {"form": form},
    )


# =====================================================
# PDF DOWNLOAD
# =====================================================


def download_invoice_pdf(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
    )

    bg_image = request.build_absolute_uri(static("images/invoice.png"))

    context = {
        "invoice": invoice,
        "invoice_no": invoice.invoice_number,
        "bg_image": bg_image,
    }

    pdf = render_to_pdf(
        "invoices/invoice_pdf.html",
        context,
    )

    if pdf:

        customer_name = slugify(invoice.customer.customer_name)

        filename = f"{invoice.invoice_number}-" f"{customer_name}.pdf"

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    return HttpResponse(
        "Error generating PDF",
        status=400,
    )
    
def invoice_detail(request, pk):

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
        ).prefetch_related(
            "items",
            "items__product",
        ),
        pk=pk,
    )

    return render(
        request,
        "invoices/partials/invoice_detail.html",
        {
            "invoice": invoice,
        },
    )

