import json

from django.db import (
    transaction,
)

from django.db.models import (
    ProtectedError,
)

from django.http import (
    HttpResponse,
    JsonResponse,
)

from products.models import (
    Product,
)

from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.templatetags.static import (
    static,
)

from django.utils.text import (
    slugify,
)


from customers.models import (
    Customer,
)


from .models import (
    Quotation,
)


from .forms import (
    QuotationForm,
    QuotationItemFormSet,
)

from django.db.models import ProtectedError
from django.template.loader import (
    render_to_string,
)
from weasyprint import HTML

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


# =====================================================
# DOWNLOAD QUOTATION PDF
# =====================================================


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
    # BACKGROUND IMAGES
    # =========================================

    header_bg = request.build_absolute_uri(static("images/quote_header.png"))

    footer_bg = request.build_absolute_uri(static("images/quote_footer.png"))

    single_bg = request.build_absolute_uri(static("images/quote_single.png"))

    # =========================================
    # QUOTATION NUMBER
    # =========================================

    quotation_no = f"CMFQ00{quotation.id}"

    # =========================================
    # BASE URL
    # =========================================

    base_url = request.build_absolute_uri("/")

    # =========================================
    # FIRST PASS CONTEXT
    # =========================================

    first_pass_context = {
        "quotation": quotation,
        "quotation_no": quotation_no,
        "header_bg": header_bg,
        "footer_bg": footer_bg,
        "single_bg": single_bg,
        "page_count": 0,
        "is_first_pass": True,
    }

    # =========================================
    # RENDER FIRST PASS HTML
    # =========================================

    first_pass_html = render_to_string(
        "quotations/quotation_pdf.html",
        first_pass_context,
        request=request,
    )

    # =========================================
    # WEASYPRINT FIRST PASS
    # =========================================

    first_pass_document = HTML(
        string=first_pass_html,
        base_url=base_url,
    ).render()

    # =========================================
    # ACTUAL PAGE COUNT
    # =========================================

    page_count = len(first_pass_document.pages)

    # =========================================
    # FINAL CONTEXT
    # =========================================

    final_context = {
        "quotation": quotation,
        "quotation_no": quotation_no,
        "header_bg": header_bg,
        "footer_bg": footer_bg,
        "single_bg": single_bg,
        "page_count": page_count,
        "is_first_pass": False,
    }

    # =========================================
    # RENDER FINAL HTML
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
        base_url=base_url,
    ).write_pdf()

    # =========================================
    # CUSTOMER NAME
    # =========================================

    customer_name = slugify(quotation.customer.customer_name)

    # =========================================
    # QUOTATION TITLE
    # =========================================

    quotation_title = slugify(quotation.title)

    # =========================================
    # FILE NAME
    # =========================================

    filename = f"{quotation_no}-" f"{customer_name}-" f"{quotation_title}.pdf"

    # =========================================
    # PDF RESPONSE
    # =========================================

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = "inline; " f'filename="{filename}"'

    return response
