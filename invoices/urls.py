from django.urls import path

from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path(
        "create/",
        views.invoice_create,
        name="invoice_create",
    ),
    path(
        "<int:pk>/edit/",
        views.invoice_update,
        name="invoice_update",
    ),
    path(
        "<int:pk>/delete/",
        views.invoice_delete,
        name="invoice_delete",
    ),
    path(
        "item-row/",
        views.invoice_item_empty_row,
        name="invoice_item_empty_row",
    ),
    path(
        "invoice/<int:pk>/pdf/",
        views.download_invoice_pdf,
        name="download_invoice_pdf",
    ),
    path(
        "<int:pk>/detail/",
        views.invoice_detail,
        name="invoice_detail",
    ),
]
