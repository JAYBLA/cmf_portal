from django.urls import path

from . import views

app_name = "customers"

urlpatterns = [

    path(
        "",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "table/",
        views.customer_table,
        name="customer_table"
    ),

    path(
        "create/",
        views.customer_create,
        name="customer_create"
    ),

    path(
        "update/<int:pk>/",
        views.customer_update,
        name="customer_update"
    ),

    path(
        "delete/<int:pk>/",
        views.customer_delete,
        name="customer_delete"
    ),

]