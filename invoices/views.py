import json
from decimal import Decimal
from pathlib import Path

from django.contrib.staticfiles import finders
from django.db import transaction
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML
from customers.models import Customer
from products.models import Product
from sales.models import SalesProductPricing
from .forms import InvoiceForm, InvoiceItemFormSet
from .models import Invoice
from utils import apply_document_backgrounds


# =====================================================
# HELPER
# =====================================================


def update_invoice_totals(invoice):

    subtotal = sum(
        (
            item.subtotal
            for item in invoice.items.all()
        ),
        Decimal("0.00"),
    )

    invoice.subtotal = subtotal

    invoice.total_amount = (
        subtotal - invoice.discount_amount
    )

    invoice.balance = (
        invoice.total_amount - invoice.amount_paid
    )

    if (
        invoice.balance <= 0
        and invoice.total_amount > 0
    ):

        invoice.status = "paid"

    elif invoice.amount_paid > 0:

        invoice.status = "partial"

    elif invoice.total_amount > 0:

        invoice.status = "unpaid"

    else:

        invoice.status = "draft"

    invoice.save()


# =====================================================
# INVOICE LIST
# =====================================================


def invoice_list(request):

    invoices = Invoice.objects.select_related(
        "customer",
    ).prefetch_related(
        "items",
    )

    context = {
        "invoices": invoices,
    }

    return render(
        request,
        "invoices/invoice_list.html",
        context,
    )


# =====================================================
# INVOICE TABLE
# =====================================================


def invoice_table(request):

    invoices = Invoice.objects.select_related(
        "customer",
    ).prefetch_related(
        "items",
    )

    context = {
        "invoices": invoices,
    }

    return render(
        request,
        "invoices/partials/invoice_table.html",
        context,
    )


# =====================================================
# CREATE INVOICE
# =====================================================


@transaction.atomic
def invoice_create(request):

    form = InvoiceForm(
        request.POST or None
    )

    formset = InvoiceItemFormSet(
        request.POST or None,
        prefix="items",
    )

    if request.method == "POST":

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()

        print(
            "FORM VALID:",
            form_valid,
        )

        print(
            "FORM ERRORS:",
            form.errors,
        )

        print(
            "FORMSET VALID:",
            formset_valid,
        )

        print(
            "FORMSET ERRORS:",
            formset.errors,
        )

        print(
            "FORMSET NON FORM ERRORS:",
            formset.non_form_errors(),
        )


        if form_valid and formset_valid:

            # ---------------------------------
            # Save invoice
            # ---------------------------------

            invoice = form.save(
                commit=False
            )

            # ---------------------------------
            # Customer
            # ---------------------------------

            customer_value = (
                form.cleaned_data[
                    "customer_text"
                ]
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

                customer, _ = (
                    Customer.objects
                    .get_or_create(
                        customer_name=customer_value
                    )
                )


            invoice.customer = customer

            invoice.save()


            # ---------------------------------
            # Save items
            # ---------------------------------

            formset.instance = invoice

            items = formset.save(
                commit=False
            )


            for item in items:

                item.invoice = invoice

                item.save()


            # ---------------------------------
            # Delete removed items
            # ---------------------------------

            for obj in formset.deleted_objects:

                obj.delete()


            # ---------------------------------
            # Update totals
            # ---------------------------------

            update_invoice_totals(
                invoice
            )


            # ---------------------------------
            # Response
            # ---------------------------------

            response = HttpResponse("")


            response["HX-Trigger"] = (
                json.dumps(
                    {
                        "recordSaved": True,
                        "refreshTable": True,
                        "showMessage": {
                            "type": "success",
                            "message": (
                                "Invoice created "
                                "successfully."
                            ),
                        },
                    }
                )
            )


            return response


    context = {
        "form": form,
        "formset": formset,
    }


    return render(
        request,
        "invoices/partials/invoice_form.html",
        context,
    )

# =====================================================
# UPDATE INVOICE
# =====================================================


@transaction.atomic
def invoice_update(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
    )

    form = InvoiceForm(
        request.POST or None,
        instance=invoice,
    )

    formset = InvoiceItemFormSet(
        request.POST or None,
        instance=invoice,
        prefix="items",
    )

    if request.method == "POST":

        if form.is_valid() and formset.is_valid():

            # ---------------------------------
            # Save invoice
            # ---------------------------------

            invoice = form.save(commit=False)

            # ---------------------------------
            # Customer
            # ---------------------------------

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

                customer, _ = (
                    Customer.objects.get_or_create(
                        customer_name=customer_value
                    )
                )

            invoice.customer = customer

            invoice.save()

            # ---------------------------------
            # Save items
            # ---------------------------------

            formset.instance = invoice

            items = formset.save(
                commit=False
            )

            for item in items:

                item.invoice = invoice

                item.save()

            # ---------------------------------
            # Delete removed items
            # ---------------------------------

            for obj in formset.deleted_objects:

                obj.delete()

            # ---------------------------------
            # Update totals
            # ---------------------------------

            update_invoice_totals(invoice)

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
                        "message": (
                            "Invoice updated successfully."
                        ),
                    },
                }
            )

            return response

    context = {
        "invoice": invoice,
        "form": form,
        "formset": formset,
    }

    return render(
        request,
        "invoices/partials/invoice_form.html",
        context,
    )


# =====================================================
# DELETE INVOICE
# =====================================================


def invoice_delete(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk,
    )


    if request.method == "POST":

        # =========================================
        # PREVENT DELETE IF RECEIPTS EXIST
        # =========================================

        if invoice.receipts.exists():

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "showMessage": {
                        "type": "error",
                        "message": (
                            f"{invoice.invoice_number} "
                            "cannot be deleted because "
                            "it already has recorded "
                            "receipts."
                        ),
                    },
                }
            )

            return response


        # =========================================
        # DELETE INVOICE
        # =========================================

        try:

            invoice.delete()


        except ProtectedError:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "showMessage": {
                        "type": "error",
                        "message": (
                            "This invoice is already "
                            "referenced by another record "
                            "and cannot be deleted."
                        ),
                    },
                }
            )

            return response


        # =========================================
        # SUCCESS RESPONSE
        # =========================================

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": (
                        "Invoice deleted successfully."
                    ),
                },
            }
        )

        return response


    context = {
        "invoice": invoice,
    }


    return render(
        request,
        "invoices/partials/invoice_delete.html",
        context,
    )


# =====================================================
# INVOICE DETAIL
# =====================================================


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

    context = {
        "invoice": invoice,
    }

    return render(
        request,
        "invoices/partials/invoice_detail.html",
        context,
    )


# =====================================================
# EMPTY ITEM ROW
# =====================================================


def invoice_item_empty_row(request):

    total_forms = int(
        request.GET.get(
            "total_forms",
            0,
        )
    )

    formset = InvoiceItemFormSet(
        prefix="items"
    )

    form = formset.empty_form

    form.prefix = (
        f"items-{total_forms}"
    )

    context = {
        "form": form,
    }

    return render(
        request,
        "invoices/partials/item_row.html",
        context,
    )


    
# =========================================
# PRODUCT EFFECTIVE SELLING PRICE
# =========================================


def product_price(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id,
    )

    try:

        pricing = SalesProductPricing.objects.get(
            product=product,
        )

    except SalesProductPricing.DoesNotExist:

        return JsonResponse(
            {
                "product_id": product.id,
                "selling_price": "0.00",
                "calculated_price": "0.00",
                "declared_price": None,
                "price_source": "none",
            }
        )


    # =========================================
    # DETERMINE EFFECTIVE PRICE
    # =========================================

    if pricing.declared_price is not None:

        effective_price = pricing.declared_price

        price_source = "declared"

    else:

        effective_price = pricing.selling_price

        price_source = "calculated"


    return JsonResponse(
        {
            "product_id": product.id,

            "selling_price": str(
                effective_price
            ),

            "calculated_price": str(
                pricing.selling_price
            ),

            "declared_price": (
                str(pricing.declared_price)
                if pricing.declared_price is not None
                else None
            ),

            "price_source": price_source,
        }
    )
    
# =====================================================
# DOWNLOAD invoice PDF
# =====================================================


def download_invoice_pdf(request, pk):

    # =========================================
    # GET invoice
    # =========================================

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            "customer",
        ).prefetch_related(
            "items",           
        ),
        pk=pk,
    )


    # =========================================
    # BACKGROUND IMAGE PATHS
    # =========================================

    header_path = finders.find(
        "images/invoice_header.png"
    )


    footer_path = finders.find(
        "images/invoice_footer.png"
    )


    single_path = finders.find(
        "images/invoice_single.png"
    )   

    # =========================================
    # VALIDATE BACKGROUND FILES
    # =========================================

    if not header_path:

        raise FileNotFoundError(
            "invoice_header.png was not found."
        )


    if not footer_path:

        raise FileNotFoundError(
            "invoice_footer.png was not found."
        )


    if not single_path:

        raise FileNotFoundError(
            "invoice_single.png was not found."
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
    # invoice NUMBER
    # =========================================

    invoice_no = invoice.invoice_number


    # =========================================
    # FIRST PAGINATION PASS
    # =========================================

    page_count = 1


    for _ in range(5):

        context = {

            "invoice": invoice,

            "invoice_no": invoice_no,

            "page_count": page_count,

        }


        html = render_to_string(
            "invoices/invoice_pdf.html",
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

        "invoice": invoice,

        "invoice_no": invoice_no,

        "page_count": page_count,

        "poppins_font": poppins_font,

    }


    # =========================================
    # FINAL HTML
    # =========================================

    final_html = render_to_string(
        "invoices/invoice_pdf.html",
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
        invoice.customer.customer_name
    )


    # =========================================
    # invoice TITLE
    # =========================================

    invoice_title = slugify(
        invoice.title
    )


    # =========================================
    # FILE NAME
    # =========================================

    filename = (

        f"{invoice_no}-"

        f"{customer_name}-"

        f"{invoice_title}.pdf"

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