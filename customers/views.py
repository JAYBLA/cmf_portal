import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import ProtectedError

from .models import Customer
from .forms import CustomerForm

# =========================================
# CUSTOMER LIST
# =========================================


def customer_list(request):

    customers = Customer.objects.all()

    context = {"customers": customers}

    return render(request, "customers/list.html", context)


# =========================================
# CUSTOMER TABLE
# =========================================


def customer_table(request):

    customers = Customer.objects.all()

    context = {"customers": customers}

    return render(request, "customers/table.html", context)


# =========================================
# CREATE CUSTOMER
# =========================================


def customer_create(request):

    form = CustomerForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Customer created successfully.",
                    },
                }
            )

            return response

    context = {"form": form}

    return render(request, "customers/form.html", context)


# =========================================
# UPDATE CUSTOMER
# =========================================


def customer_update(request, pk):

    customer = get_object_or_404(Customer, pk=pk)

    form = CustomerForm(request.POST or None, instance=customer)

    if request.method == "POST":

        if form.is_valid():

            form.save()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Customer updated successfully.",
                    },
                }
            )

            return response

    context = {"form": form, "customer": customer}

    return render(request, "customers/form.html", context)


# =========================================
# DELETE CUSTOMER
# =========================================


def customer_delete(request, pk):

    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":

        try:

            customer.delete()

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "recordSaved": True,
                    "refreshTable": True,
                    "showMessage": {
                        "type": "success",
                        "message": "Customer deleted successfully.",
                    },
                }
            )

            return response

        except ProtectedError:

            response = HttpResponse("")

            response["HX-Trigger"] = json.dumps(
                {
                    "showMessage": {
                        "type": "error",
                        "message": (
                            "This customer is already "
                            "used in invoices and "
                            "cannot be deleted."
                        ),
                    }
                }
            )

            return response

    context = {"customer": customer}

    return render(request, "customers/delete.html", context)
