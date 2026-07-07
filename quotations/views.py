import json
from pathlib import Path
from django import forms
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
from .forms import QuotationForm, QuotationItemFormSet
from .models import Quotation
from utils import apply_document_backgrounds


# =====================================================
# QUOTATION LIST
# =====================================================


def quotation_list(request):

    quotations = Quotation.objects.select_related(
        "customer",
    ).prefetch_related(
        "items",
        "items__product",
        "payment_terms",
    )

    context = {
        "quotations": quotations,
    }

    return render(
        request,
        "quotations/quotation_list.html",
        context,
    )


# =====================================================
# QUOTATION TABLE
# =====================================================


def quotation_table(request):

    quotations = Quotation.objects.select_related(
        "customer",
    ).prefetch_related(
        "items",
        "items__product",
        "payment_terms",
    )

    context = {
        "quotations": quotations,
    }

    return render(
        request,
        "quotations/partials/quotation_table.html",
        context,
    )


# =====================================================
# CREATE QUOTATION
# =====================================================


@transaction.atomic
def quotation_create(request):

    form = QuotationForm(
        request.POST or None,
    )

    formset = QuotationItemFormSet(
        request.POST or None,
        prefix="items",
    )

    if request.method == "POST":

        # =========================================
        # VALIDATE
        # =========================================

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

        # =========================================
        # SAVE
        # =========================================

        if form_valid and formset_valid:

            # ---------------------------------
            # Prepare quotation
            # ---------------------------------

            quotation = form.save(
                commit=False,
            )

            # ---------------------------------
            # Customer
            # ---------------------------------

            customer_value = form.cleaned_data["customer_text"].strip()

            try:

                customer = Customer.objects.get(pk=int(customer_value))

            except (
                ValueError,
                TypeError,
                Customer.DoesNotExist,
            ):

                customer, _ = Customer.objects.get_or_create(
                    customer_name=(customer_value)
                )

            quotation.customer = customer

            # ---------------------------------
            # Save quotation
            # ---------------------------------

            quotation.save()

            # ---------------------------------
            # Save many-to-many fields
            # ---------------------------------

            form.save_m2m()

            # ---------------------------------
            # Save quotation items
            # ---------------------------------

            formset.instance = quotation

            items = formset.save(
                commit=False,
            )

            for item in items:

                item.quotation = quotation

                item.save()

            # ---------------------------------
            # Delete removed items
            # ---------------------------------

            for obj in formset.deleted_objects:

                obj.delete()

            # ---------------------------------
            # Save formset many-to-many
            # ---------------------------------

            formset.save_m2m()

            # ---------------------------------
            # Response
            # ---------------------------------

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Quotation created " "successfully."),
                    },
                }
            )

            return response

    # =========================================
    # CONTEXT
    # =========================================

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


@transaction.atomic
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

            # =================================
            # SAVE QUOTATION
            # =================================

            quotation = form.save(commit=False)

            # =================================
            # CUSTOMER
            # =================================

            customer_value = form.cleaned_data["customer_text"].strip()

            try:

                customer = Customer.objects.get(pk=int(customer_value))

            except (
                ValueError,
                TypeError,
                Customer.DoesNotExist,
            ):

                customer, _ = Customer.objects.get_or_create(
                    customer_name=(customer_value)
                )

            quotation.customer = customer

            quotation.save()

            # =================================
            # SAVE MANY-TO-MANY
            # =================================

            form.save_m2m()

            # =================================
            # ATTACH FORMSET
            # =================================

            formset.instance = quotation

            # =================================
            # PREPARE FORMSET OBJECTS
            #
            # THIS CREATES deleted_objects
            # =================================

            items = formset.save(commit=False)

            # =================================
            # DELETE REMOVED ITEMS
            # =================================

            for obj in formset.deleted_objects:

                # =================================
                # PREVENT DELETE IF DELIVERED
                # =================================

                if obj.delivery_items.exists():

                    raise forms.ValidationError(
                        (
                            f"{obj.item_name} cannot "
                            "be deleted because it "
                            "has already been used "
                            "in a delivery note."
                        )
                    )

                obj.delete()

            # =================================
            # SAVE ITEMS
            # =================================

            for item in items:

                item.quotation = quotation

                item.save()

            # =================================
            # SAVE FORMSET M2M
            # =================================

            formset.save_m2m()

            # =================================
            # RESPONSE
            # =================================

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": ("Quotation updated " "successfully."),
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
        ("quotations/partials/" "quotation_form.html"),
        context,
    )


# =====================================================
# DELETE QUOTATION
# =====================================================


def quotation_delete(
    request,
    pk,
):

    quotation = get_object_or_404(
        Quotation,
        pk=pk,
    )

    if request.method == "POST":

        # =========================================
        # DELETE QUOTATION
        # =========================================

        try:

            quotation.delete()

        except ProtectedError:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "showMessage": {
                        "type": "error",
                        "message": (
                            "This quotation is already "
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
                    "message": ("Quotation deleted " "successfully."),
                },
            }
        )

        return response

    # =========================================
    # CONTEXT
    # =========================================

    context = {
        "quotation": quotation,
    }

    return render(
        request,
        "quotations/partials/quotation_delete.html",
        context,
    )


# =====================================================
# QUOTATION DETAIL
# =====================================================


def quotation_detail(
    request,
    pk,
):

    quotation = get_object_or_404(
        (
            Quotation.objects.select_related(
                "customer",
            ).prefetch_related(
                "items",
                "items__product",
                "payment_terms",
            )
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
# EMPTY QUOTATION ITEM ROW
# =====================================================


def quotation_item_empty_row(request):

    total_forms = int(
        request.GET.get(
            "total_forms",
            0,
        )
    )

    formset = QuotationItemFormSet(
        prefix="items",
    )

    form = formset.empty_form

    form.prefix = f"items-{total_forms}"

    context = {
        "form": form,
    }

    return render(
        request,
        "quotations/partials/item_row.html",
        context,
    )


# =====================================================
# PRODUCT STATE
# =====================================================


def product_state(
    request,
    product_id,
):

    product = get_object_or_404(
        Product,
        pk=product_id,
    )

    return JsonResponse(
        {
            "product_id": product.id,
            "is_tangible": product.is_tangible,
        }
    )

def download_quotation_pdf(request, pk):

    # =========================================
    # GET QUOTATION
    # =========================================

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "customer",
        ).prefetch_related(
            "items",
            "payment_terms",
        ),
        pk=pk,
    )


    # =========================================
    # BACKGROUND IMAGE PATHS
    # =========================================

    header_path = finders.find(
        "images/quote_header.png"
    )

    footer_path = finders.find(
        "images/quote_footer.png"
    )

    single_path = finders.find(
        "images/quotation_single.png"
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
    # BACKGROUND FILE URIS
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
    # FONT PATH
    # =========================================

    poppins_font_path = finders.find(
        "fonts/poppins-regular.ttf"
    )


    # =========================================
    # VALIDATE FONT
    # =========================================

    if not poppins_font_path:

        raise FileNotFoundError(
            "poppins-regular.ttf was not found."
        )


    # =========================================
    # FONT FILE URI
    # =========================================

    poppins_font = Path(
        poppins_font_path
    ).resolve().as_uri()


    # =========================================
    # QUOTATION NUMBER
    # =========================================

    quotation_no = (
        f"CMFQ00{quotation.id}"
    )


    # =========================================
    # FIRST PAGINATION PASS
    # =========================================

    page_count = 1


    for _ in range(5):

        context = {

            "quotation": quotation,

            "quotation_no": quotation_no,

            "page_count": page_count,

            "poppins_font": poppins_font,

            "header_bg": header_bg,

            "footer_bg": footer_bg,

            "single_bg": single_bg,

        }


        html = render_to_string(
            "quotations/quotation_pdf.html",
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

        "quotation": quotation,

        "quotation_no": quotation_no,

        "page_count": page_count,

        "poppins_font": poppins_font,

        "header_bg": header_bg,

        "footer_bg": footer_bg,

        "single_bg": single_bg,

    }


    # =========================================
    # FINAL HTML
    # =========================================

    final_html = render_to_string(
        "quotations/quotation_pdf.html",
        final_context,
        request=request,
    )


    # =========================================
    # GENERATE FINAL PDF
    # =========================================

    pdf = HTML(
        string=final_html,
    ).write_pdf()


    # =========================================
    # CUSTOMER NAME
    # =========================================

    customer_name = slugify(
        quotation.customer.customer_name
    )


    # =========================================
    # QUOTATION TITLE
    # =========================================

    quotation_title = slugify(
        quotation.title
    )


    # =========================================
    # FILE NAME
    # =========================================

    filename = (

        f"{quotation_no}-"

        f"{customer_name}-"

        f"{quotation_title}.pdf"

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