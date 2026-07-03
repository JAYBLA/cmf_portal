from django.urls import path

from . import views


app_name = "invoices"


urlpatterns = [

    # =====================================================
    # INVOICE LIST
    # =====================================================

    path(
        "",
        views.invoice_list,
        name="invoice_list",
    ),

    # =====================================================
    # INVOICE TABLE
    # =====================================================

    path(
        "table/",
        views.invoice_table,
        name="invoice_table",
    ),

    # =====================================================
    # CREATE INVOICE
    # =====================================================

    path(
        "create/",
        views.invoice_create,
        name="invoice_create",
    ),

    # =====================================================
    # UPDATE INVOICE
    # =====================================================

    path(
        "update/<int:pk>/",
        views.invoice_update,
        name="invoice_update",
    ),

    # =====================================================
    # DELETE INVOICE
    # =====================================================

    path(
        "delete/<int:pk>/",
        views.invoice_delete,
        name="invoice_delete",
    ),

    # =====================================================
    # INVOICE DETAIL
    # =====================================================

    path(
        "detail/<int:pk>/",
        views.invoice_detail,
        name="invoice_detail",
    ),

    # =====================================================
    # EMPTY ITEM ROW
    # =====================================================

    path(
        "item/empty-row/",
        views.invoice_item_empty_row,
        name="invoice_item_empty_row",
    ),

    # =====================================================
    # DOWNLOAD INVOICE PDF
    # =====================================================

    path(
        "download/<int:pk>/",
        views.download_invoice_pdf,
        name="download_invoice_pdf",
    ),

]