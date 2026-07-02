import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import VoucherForm, VoucherItemFormSet
from .models import Voucher

# =========================================
# VOUCHER LIST
# =========================================


def voucher_list(request):

    vouchers = Voucher.objects.all()

    return render(
        request,
        "vouchers/voucher_list.html",
        {
            "vouchers": vouchers,
        },
    )


# =========================================
# VOUCHER TABLE
# =========================================


def voucher_table(request):

    vouchers = Voucher.objects.all()

    return render(
        request,
        "vouchers/partials/voucher_table.html",
        {
            "vouchers": vouchers,
        },
    )


# =========================================
# CREATE
# =========================================


def voucher_create(request):

    if request.method == "POST":

        form = VoucherForm(request.POST)

        if form.is_valid():

            voucher = form.save(commit=False)

            voucher.subtotal = 0
            voucher.total_amount = 0

            voucher.save()

            formset = VoucherItemFormSet(
                request.POST,
                instance=voucher,
                prefix="items",
            )

            if formset.is_valid():

                formset.save()

                total = sum(item.amount for item in voucher.items.all())

                voucher.subtotal = total
                voucher.total_amount = total

                voucher.save(
                    update_fields=[
                        "subtotal",
                        "total_amount",
                    ]
                )

                response = HttpResponse("")

                response["HX-Trigger"] = json.dumps(
                    {
                        "recordSaved": True,
                        "refreshTable": True,
                        "showMessage": {
                            "type": "success",
                            "message": "Voucher created successfully.",
                        },
                    }
                )

                return response

        else:

            formset = VoucherItemFormSet(
                request.POST,
                prefix="items",
            )

    else:

        form = VoucherForm()

        formset = VoucherItemFormSet(
            prefix="items",
        )

    return render(
        request,
        "vouchers/partials/voucher_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )


# =========================================
# UPDATE
# =========================================


def voucher_update(request, pk):

    voucher = get_object_or_404(
        Voucher,
        pk=pk,
    )

    if request.method == "POST":

        form = VoucherForm(
            request.POST,
            instance=voucher,
        )

        formset = VoucherItemFormSet(
            request.POST,
            instance=voucher,
            prefix="items",
        )

        if form.is_valid() and formset.is_valid():

            form.save()

            formset.save()

            total = sum(item.amount for item in voucher.items.all())

            voucher.subtotal = total
            voucher.total_amount = total

            voucher.save(
                update_fields=[
                    "subtotal",
                    "total_amount",
                ]
            )

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Voucher updated successfully.",
                    },
                }
            )

            return response

    else:

        form = VoucherForm(
            instance=voucher,
        )

        formset = VoucherItemFormSet(
            instance=voucher,
            prefix="items",
        )

    return render(
        request,
        "vouchers/partials/voucher_form.html",
        {
            "form": form,
            "formset": formset,
            "voucher": voucher,
        },
    )


# =========================================
# DELETE
# =========================================


def voucher_delete(request, pk):

    voucher = get_object_or_404(
        Voucher,
        pk=pk,
    )

    if request.method == "POST":

        voucher.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = json.dumps(
            {
                "recordSaved": True,
                "refreshTable": True,
                "showMessage": {
                    "type": "success",
                    "message": "Voucher deleted successfully.",
                },
            }
        )

        return response

    return render(
        request,
        "vouchers/partials/voucher_delete.html",
        {
            "voucher": voucher,
        },
    )


# =========================================
# DETAIL
# =========================================


def voucher_detail(request, pk):

    voucher = get_object_or_404(
        Voucher.objects.select_related("approved_by").prefetch_related("items"),
        pk=pk,
    )

    return render(
        request,
        "vouchers/partials/voucher_detail.html",
        {
            "voucher": voucher,
        },
    )


# =====================================================
# DOWNLOAD
# =====================================================


def download_voucher_pdf(request, pk):

    voucher = get_object_or_404(
        Voucher,
        pk=pk,
    )

    bg_image = request.build_absolute_uri(static("images/voucher.png"))

    context = {
        "voucher": voucher,
        "voucher_no": voucher.voucher_number,
        "bg_image": bg_image,
    }

    pdf = render_to_pdf(
        "vouchers/voucher_pdf.html",
        context,
    )

    if pdf:

        payee_name = slugify(voucher.payee_name)

        filename = f"{voucher.voucher_number}-" f"{payee_name}.pdf"

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        # Download PDF
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        # Preview in browser
        # response["Content-Disposition"] = (
        #     f'inline; filename="{filename}"'
        # )

        return response

    return HttpResponse(
        "Error generating PDF",
        status=400,
    )
