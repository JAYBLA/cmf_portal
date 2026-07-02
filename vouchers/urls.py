from django.urls import path

from . import views

app_name = "vouchers"

urlpatterns = [
    path(
        "",
        views.voucher_list,
        name="voucher_list",
    ),
    path(
        "create/",
        views.voucher_create,
        name="voucher_create",
    ),
    path(
        "<int:pk>/edit/",
        views.voucher_update,
        name="voucher_update",
    ),
    path(
        "<int:pk>/delete/",
        views.voucher_delete,
        name="voucher_delete",
    ),
    path(
        "table/",
        views.voucher_table,
        name="voucher_table",
    ),
    path(
        "<int:pk>/pdf/",
        views.download_voucher_pdf,
        name="download_voucher_pdf",
    ),
    path(
        "<int:pk>/detail/",
        views.voucher_detail,
        name="voucher_detail",
    ),
]
