from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Supplier
from .forms import SupplierForm


# =========================================
# LIST
# =========================================

def supplier_list(request):

    suppliers = Supplier.objects.all()

    context = {
        "suppliers": suppliers
    }

    return render(
        request,
        "suppliers/supplier_list.html",
        context
    )


# =========================================
# CREATE
# =========================================

def supplier_create(request):

    form = SupplierForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            supplier = form.save()

            context = {
                "supplier": supplier
            }

            response = render(
                request,
                "suppliers/partials/supplier_row.html",
                context
            )

            response["HX-Trigger"] = "closeModal"

            return response

    context = {
        "form": form
    }

    return render(
        request,
        "suppliers/partials/supplier_form.html",
        context
    )


# =========================================
# UPDATE
# =========================================

def supplier_update(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    form = SupplierForm(
        request.POST or None,
        instance=supplier
    )

    if request.method == "POST":

        if form.is_valid():

            supplier = form.save()

            context = {
                "supplier": supplier
            }

            response = render(
                request,
                "suppliers/partials/supplier_row.html",
                context
            )

            response["HX-Trigger"] = "closeModal"

            return response

    context = {
        "form": form,
        "supplier": supplier
    }

    return render(
        request,
        "suppliers/partials/supplier_form.html",
        context
    )


# =========================================
# DELETE
# =========================================

def supplier_delete(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == "POST":

        supplier.delete()

        response = HttpResponse("")

        response["HX-Trigger"] = "closeModal"

        return response

    context = {
        "supplier": supplier
    }

    return render(
        request,
        "suppliers/partials/supplier_delete.html",
        context
    )