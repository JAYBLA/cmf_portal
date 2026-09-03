import json
from datetime import date

from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import (
    LendingForm,
    LendingItemAddFormSet,
    LendingItemFormSet,
    LendingInlineItemForm,
)
from .models import Lending, LendingItem


def _saved_response(message):
    response = HttpResponse("")
    response["HX-Trigger"] = json.dumps({
        "recordSaved": True,
        "refreshTable": True,
        "showMessage": {"type": "success", "message": message},
    })
    return response


def _filtered_lendings(request):
    lendings = Lending.objects.select_related("customer").prefetch_related("items")
    customer = request.GET.get("customer", "").strip()
    item = request.GET.get("item", "").strip()
    status = request.GET.get("status", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    if customer:
        lendings = lendings.filter(
            Q(customer__customer_name__icontains=customer)
            | Q(customer__company_name__icontains=customer)
        )
    if item:
        lendings = lendings.filter(
            Q(items__item_name__icontains=item) | Q(items__asset_tag__icontains=item)
        )
    if date_from:
        lendings = lendings.filter(lending_date__gte=date_from)
    if date_to:
        lendings = lendings.filter(lending_date__lte=date_to)
    if status == "overdue":
        lendings = lendings.filter(due_date__lt=date.today()).exclude(
            return_status=Lending.ReturnStatus.RETURNED
        )
    elif status in (Lending.ReturnStatus.ACTIVE, Lending.ReturnStatus.PARTIAL):
        lendings = lendings.filter(return_status=status).filter(
            Q(due_date__isnull=True) | Q(due_date__gte=date.today())
        )
    elif status:
        lendings = lendings.filter(return_status=status)

    lendings = lendings.distinct()
    lending_ids = lendings.values("pk")
    item_totals = LendingItem.objects.filter(lending_id__in=lending_ids).aggregate(
        total=Sum("quantity"),
        returned=Sum("returned_quantity"),
    )
    total_quantity = item_totals["total"] or 0
    returned_quantity = item_totals["returned"] or 0
    totals = {
        "lending_count": lendings.count(),
        "total_quantity": total_quantity,
        "returned_quantity": returned_quantity,
        "outstanding_quantity": max(total_quantity - returned_quantity, 0),
    }
    return {
        "lendings": lendings,
        "totals": totals,
        "status_choices": (
            (Lending.ReturnStatus.ACTIVE, "Active"),
            ("overdue", "Overdue"),
            (Lending.ReturnStatus.PARTIAL, "Partially returned"),
            (Lending.ReturnStatus.RETURNED, "Returned"),
        ),
    }


def lending_list(request):
    return render(request, "lendings/lending_list.html", _filtered_lendings(request))


def lending_table(request):
    return render(request, "lendings/partials/lending_results.html", _filtered_lendings(request))


def lending_create(request):
    form = LendingForm(request.POST or None)
    formset = LendingItemFormSet(request.POST or None, prefix="items")
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            lending = form.save()
            formset.instance = lending
            formset.save()
            lending.refresh_return_status()
        return _saved_response("Lending and its items created successfully.")
    return render(
        request,
        "lendings/partials/lending_form.html",
        {"form": form, "formset": formset},
    )


def lending_update(request, pk):
    lending = get_object_or_404(Lending, pk=pk)
    form = LendingForm(request.POST or None, instance=lending)
    formset = LendingItemFormSet(
        request.POST or None,
        instance=lending,
        prefix="items",
    )
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            form.save()
            formset.save()
            lending.refresh_return_status()
        return _saved_response("Lending and its items updated successfully.")
    return render(
        request,
        "lendings/partials/lending_form.html",
        {"form": form, "formset": formset, "lending": lending},
    )


def lending_delete(request, pk):
    lending = get_object_or_404(Lending, pk=pk)
    if request.method == "POST":
        lending.delete()
        return _saved_response("Lending deleted successfully.")
    return render(request, "lendings/partials/lending_delete.html", {"lending": lending})


def item_list(request, lending_id):
    lending = get_object_or_404(Lending.objects.select_related("customer"), pk=lending_id)
    return render(request, "lendings/item_list.html", {"lending": lending, "items": lending.items.all()})


def item_table(request, lending_id):
    lending = get_object_or_404(Lending, pk=lending_id)
    return render(request, "lendings/partials/item_table.html", {"lending": lending, "items": lending.items.all()})


def item_create(request, lending_id):
    lending = get_object_or_404(Lending, pk=lending_id)
    formset = LendingItemAddFormSet(request.POST or None, instance=lending, prefix="items")
    if request.method == "POST" and formset.is_valid():
        with transaction.atomic():
            formset.save()
            lending.refresh_return_status()
        return _saved_response("Lending items added successfully.")
    return render(request, "lendings/partials/item_formset.html", {"formset": formset, "lending": lending})


def item_update(request, pk):
    item = get_object_or_404(LendingItem.objects.select_related("lending"), pk=pk)
    form = LendingInlineItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            item = form.save()
            item.lending.refresh_return_status()
        return _saved_response("Lending item updated successfully.")
    return render(request, "lendings/partials/item_form.html", {"form": form, "item": item, "lending": item.lending})


def item_delete(request, pk):
    item = get_object_or_404(LendingItem.objects.select_related("lending"), pk=pk)
    lending = item.lending
    if request.method == "POST":
        with transaction.atomic():
            item.delete()
            lending.refresh_return_status()
        return _saved_response("Lending item deleted successfully.")
    return render(request, "lendings/partials/item_delete.html", {"item": item})
