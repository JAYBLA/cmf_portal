from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("table/", views.project_table, name="project_table"),
    path("create/", views.project_create, name="project_create"),
    path("<int:pk>/update/", views.project_update, name="project_update"),
    path("<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("<int:project_id>/expenses/", views.expense_list, name="expense_list"),
    path("<int:project_id>/expenses/table/", views.expense_table, name="expense_table"),
    path("<int:project_id>/expenses/create/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/update/", views.expense_update, name="expense_update"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
]
