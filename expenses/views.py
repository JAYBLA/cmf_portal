import json

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from customers.models import Customer

from .forms import ExpenseForm
from .models import Expense


def expense_list(request):
    return render(
        request,
        "expenses/expense_list.html",
        {"expenses": Expense.objects.all()},
    )


def expense_table(request):
    return render(
        request,
        "expenses/partials/expense_table.html",
        {"expenses": Expense.objects.all()},
    )


def _render_expense_form(request, context):
    response = render(request, "expenses/partials/expense_form.html", context)
    if request.method == "POST":
        response["HX-Retarget"] = "#modal-body"
        response["HX-Reswap"] = "innerHTML"
    return response


def _resolve_payee(value):
    try:
        return Customer.objects.get(pk=int(value))
    except (ValueError, TypeError, Customer.DoesNotExist):
        existing = Customer.objects.filter(customer_name__iexact=value).first()
        if existing:
            return existing
        return Customer.objects.create(customer_name=value)


@transaction.atomic
def expense_create(request):
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.payee = _resolve_payee(form.cleaned_data["payee_text"])
        expense.save()
        return _saved_response("Expense created successfully.")
    return _render_expense_form(request, {"form": form})


@transaction.atomic
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    old_document = expense.supporting_document
    form = ExpenseForm(
        request.POST or None,
        request.FILES or None,
        instance=expense,
    )
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.payee = _resolve_payee(form.cleaned_data["payee_text"])
        expense.save()
        if old_document and old_document != expense.supporting_document:
            transaction.on_commit(lambda: old_document.delete(save=False))
        return _saved_response("Expense updated successfully.")
    return _render_expense_form(request, {"form": form, "expense": expense})


@transaction.atomic
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        document = expense.supporting_document
        expense.delete()
        if document:
            transaction.on_commit(lambda: document.delete(save=False))
        return _saved_response("Expense deleted successfully.")
    return render(
        request,
        "expenses/partials/expense_delete.html",
        {"expense": expense},
    )


def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(
        request,
        "expenses/partials/expense_detail.html",
        {"expense": expense},
    )


def _saved_response(message):
    response = HttpResponse("")
    response["HX-Trigger"] = json.dumps(
        {
            "recordSaved": True,
            "refreshTable": True,
            "showMessage": {"type": "success", "message": message},
        }
    )
    return response
