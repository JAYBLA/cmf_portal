# views.py

import json

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import *
from .forms import *
from django.db.models import ProtectedError

# =========================================
# PRODUCT LIST
# =========================================


def product_list(request):

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "products/product_list.html", context)


# =========================================
# PRODUCT TABLE PARTIAL
# =========================================


def product_table(request):

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "products/partials/product_table.html", context)


# =========================================
# CREATE PRODUCT
# =========================================


def product_create(request):

    form = ProductForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True
                }
            )

            return response

    context = {"form": form}

    return render(request, "products/partials/product_form.html", context)


# =========================================
# UPDATE PRODUCT
# =========================================


def product_update(request, pk):

    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(request.POST or None, instance=product)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True
                }
            )

            return response

    context = {"form": form, "product": product}

    return render(request, "products/partials/product_form.html", context)


# =========================================
# DELETE PRODUCT
# =========================================


def product_delete(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":

        try:

            product.delete()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Product deleted successfully.",
                    },
                }
            )

            return response

        except ProtectedError:

            response = HttpResponse("")

            response.headers["HX-Trigger"] = json.dumps(
                {
                    "closeModal": True,
                    "showMessage": {
                        "type": "error",
                        "message": (
                            "This product is already used "
                            "in transactions and cannot "
                            "be deleted."
                        ),
                    },
                }
            )
            return response

    context = {"product": product}

    return render(request, "products/partials/product_delete.html", context)


# =========================================
# PRODUCT TABLE PARTIAL
# =========================================


def product_table(request):

    products = Product.objects.all()

    context = {"products": products}

    return render(request, "products/partials/product_table.html", context)

# =========================================
# STOCK MOVEMENT LIST
# =========================================

def stock_movement_list(request):

    stock_movements = (
        StockMovement.objects
        .select_related("product")
    )

    context = {

        "stock_movements": stock_movements

    }

    return render(
        request,
        "products/stock_movements/list.html",
        context
    )



# =========================================
# STOCK MOVEMENT TABLE
# =========================================

def stock_movement_table(request):

    stock_movements = (
        StockMovement.objects
        .select_related("product")
    )

    context = {

        "stock_movements": stock_movements

    }

    return render(
        request,
        "products/stock_movements/table.html",
        context
    )
    

