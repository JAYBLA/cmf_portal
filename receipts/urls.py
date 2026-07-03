from django.urls import path

from . import views

app_name = "receipts"


urlpatterns = [
    # =========================================
    # RECEIPT LIST
    # =========================================
    path(
        "",
        views.receipt_list,
        name="receipt_list",
    ),
    # =========================================
    # RECEIPT TABLE
    # =========================================
    path(
        "table/",
        views.receipt_table,
        name="receipt_table",
    ),
    # =========================================
    # CREATE RECEIPT
    # =========================================
    path(
        "create/",
        views.receipt_create,
        name="receipt_create",
    ),
    # =========================================
    # UPDATE RECEIPT
    # =========================================
    path(
        "update/<int:pk>/",
        views.receipt_update,
        name="receipt_update",
    ),
    # =========================================
    # DELETE RECEIPT
    # =========================================
    path(
        "delete/<int:pk>/",
        views.receipt_delete,
        name="receipt_delete",
    ),
    # =========================================
    # RECEIPT DETAIL
    # =========================================
    path(
        "detail/<int:pk>/",
        views.receipt_detail,
        name="receipt_detail",
    ),
    # =========================================
    # DOWNLOAD RECEIPT PDF
    # =========================================
    path(
        "download/<int:pk>/",
        views.download_receipt_pdf,
        name="download_receipt_pdf",
    ),
]
