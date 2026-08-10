import json
from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import ProjectExpenseForm, ProjectExpenseFormSet, ProjectForm
from .models import Project, ProjectExpense


def _filtered_projects(request):
    expense_type = request.GET.get("expense_type", "").strip()
    expense_filter = Q()
    if expense_type:
        expense_filter = Q(expenses__expense_type=expense_type)

    projects = Project.objects.all()
    if expense_type:
        projects = projects.filter(expenses__expense_type=expense_type)

    projects = projects.annotate(
        filtered_expense_total=Coalesce(
            Sum("expenses__amount", filter=expense_filter),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
    )

    text_filters = {
        "project_name": "project_name__icontains",
        "client_name": "client_name__icontains",
        "description": "description__icontains",
        "status": "status",
        "start_date_from": "start_date__gte",
        "start_date_to": "start_date__lte",
        "end_date_from": "end_date__gte",
        "end_date_to": "end_date__lte",
        "budget_min": "budget__gte",
        "budget_max": "budget__lte",
    }
    for parameter, lookup in text_filters.items():
        value = request.GET.get(parameter, "").strip()
        if value:
            projects = projects.filter(**{lookup: value})

    projects = projects.annotate(
        filtered_profit=ExpressionWrapper(
            Coalesce(
                "budget",
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
            - Coalesce(
                "filtered_expense_total",
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            ),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
    ).distinct()

    totals = projects.aggregate(
        total_budget=Coalesce(
            Sum("budget"),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
    )
    filtered_expenses = ProjectExpense.objects.filter(
        project_id__in=projects.values("pk"),
    )
    if expense_type:
        filtered_expenses = filtered_expenses.filter(expense_type=expense_type)
    totals["total_cost"] = filtered_expenses.aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
    )["total"]
    totals["project_count"] = projects.count()
    totals["total_profit"] = totals["total_budget"] - totals["total_cost"]

    return {
        "projects": projects,
        "totals": totals,
        "status_choices": Project.Status.choices,
        "expense_type_choices": ProjectExpense.ExpenseType.choices,
        "active_expense_type": expense_type,
    }


def project_list(request):
    return render(request, "projects/project_list.html", _filtered_projects(request))


def project_table(request):
    return render(
        request,
        "projects/partials/project_results.html",
        _filtered_projects(request),
    )


def _saved_response(message):
    response = HttpResponse("")
    response["HX-Trigger"] = json.dumps({
        "recordSaved": True,
        "refreshTable": True,
        "showMessage": {"type": "success", "message": message},
    })
    return response


def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return _saved_response("Project created successfully.")
    return render(request, "projects/partials/project_form.html", {"form": form})


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        return _saved_response("Project updated successfully.")
    return render(request, "projects/partials/project_form.html", {"form": form, "project": project})


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return _saved_response("Project deleted successfully.")
    return render(request, "projects/partials/project_delete.html", {"project": project})


def expense_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, "projects/expense_list.html", {"project": project, "expenses": project.expenses.all()})


def expense_table(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, "projects/partials/expense_table.html", {"project": project, "expenses": project.expenses.all()})


def expense_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    formset = ProjectExpenseFormSet(request.POST or None, instance=project, prefix="expenses")
    if request.method == "POST" and formset.is_valid():
        formset.save()
        return _saved_response("Project expenses added successfully.")
    return render(request, "projects/partials/expense_formset.html", {"formset": formset, "project": project})


def expense_update(request, pk):
    expense = get_object_or_404(ProjectExpense, pk=pk)
    form = ProjectExpenseForm(request.POST or None, instance=expense)
    if request.method == "POST" and form.is_valid():
        form.save()
        return _saved_response("Project expense updated successfully.")
    return render(request, "projects/partials/expense_form.html", {"form": form, "project": expense.project, "expense": expense})


def expense_delete(request, pk):
    expense = get_object_or_404(ProjectExpense, pk=pk)
    if request.method == "POST":
        expense.delete()
        return _saved_response("Project expense deleted successfully.")
    return render(request, "projects/partials/expense_delete.html", {"expense": expense})
