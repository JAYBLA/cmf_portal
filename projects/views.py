import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import ProjectExpenseForm, ProjectExpenseFormSet, ProjectForm
from .models import Project, ProjectExpense


def project_list(request):
    return render(request, "projects/project_list.html", {"projects": Project.objects.all()})


def project_table(request):
    return render(request, "projects/partials/project_table.html", {"projects": Project.objects.all()})


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
