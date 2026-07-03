import json

from django.shortcuts import (
    render,
    get_object_or_404
)

from django.http import HttpResponse

from django.db.models import ProtectedError

from .models import Supplier

from .forms import SupplierForm


# =========================================
# LIST
# =========================================

def supplier_list(request):

    suppliers = Supplier.objects.all().order_by('-created_at')

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

    form = SupplierForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Supplier created successfully."

                }

            })

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

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Supplier updated successfully."

                }

            })

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

        try:

            supplier.delete()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "recordSaved": True,

                "refreshTable": True,

                "showMessage": {

                    "type": "success",

                    "message":
                        "Supplier deleted successfully."

                }

            })

            return response

        except ProtectedError:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps({

                "showMessage": {

                    "type": "error",

                    "message":
                        (
                            "This supplier is already "
                            "used in transactions and "
                            "cannot be deleted."
                        )

                }

            })

            return response

    context = {
        "supplier": supplier
    }

    return render(
        request,
        "suppliers/partials/supplier_delete.html",
        context
    )
    
# =========================================
# SUPPLIER TABLE
# =========================================

def supplier_table(request):

    suppliers = Supplier.objects.all().order_by('-created_at')

    context = {

        "suppliers": suppliers

    }

    return render(

        request,

        "suppliers/partials/supplier_table.html",

        context
    )