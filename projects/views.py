import json
from decimal import Decimal
from pathlib import Path

from django.contrib.staticfiles import finders
from django.db.models import DecimalField, ExpressionWrapper, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.text import slugify
from weasyprint import HTML

from utils import apply_document_backgrounds

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


def download_project_pdf(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related("expenses"), pk=pk)
    header_path = finders.find("images/project_header.png")
    footer_path = finders.find("images/project_footer.png")
    font_path = finders.find("fonts/Poppins-Regular.ttf")
    semibold_font_path = finders.find("fonts/Poppins-SemiBold.ttf")
    bold_font_path = finders.find("fonts/Poppins-Bold.ttf")
    project_pdf_css_path = finders.find("css/project_pdf.css")

    if not header_path or not footer_path or not project_pdf_css_path:
        raise FileNotFoundError("Project PDF header, footer, or stylesheet was not found.")

    expenses = list(project.expenses.all())
    total_expenses = sum((expense.amount for expense in expenses), Decimal("0.00"))
    context = {
        "project": project,
        "expenses": expenses,
        "total_expenses": total_expenses,
        "profit": (project.budget or Decimal("0.00")) - total_expenses,
        "poppins_font": Path(font_path).resolve().as_uri() if font_path else None,
        "poppins_semibold_font": Path(semibold_font_path).resolve().as_uri() if semibold_font_path else None,
        "poppins_bold_font": Path(bold_font_path).resolve().as_uri() if bold_font_path else None,
        "project_pdf_css": Path(project_pdf_css_path).resolve().as_uri(),
    }
    html = render_to_string("projects/project_pdf.html", context, request=request)
    content_pdf = HTML(string=html).write_pdf()
    pdf = apply_document_backgrounds(
        content_pdf=content_pdf,
        header_bg=Path(header_path).resolve().as_uri(),
        footer_bg=Path(footer_path).resolve().as_uri(),
    )
    project_title = slugify(project.project_name) or "project"
    customer_name = slugify(project.client_name) or "customer"
    filename = f"CMFP00{project.pk}-{project_title}-to-{customer_name}.pdf"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


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
