from django.urls import path

from . import views


app_name = "quotations"


urlpatterns = [

    # =========================================
    # QUOTATION LIST
    # =========================================

    path(
        "",
        views.quotation_list,
        name="quotation_list",
    ),


    # =========================================
    # QUOTATION TABLE
    # =========================================

    path(
        "table/",
        views.quotation_table,
        name="quotation_table",
    ),


    # =========================================
    # CREATE QUOTATION
    # =========================================

    path(
        "create/",
        views.quotation_create,
        name="quotation_create",
    ),


    # =========================================
    # EMPTY QUOTATION ITEM ROW
    # =========================================

    path(
        "item/empty-row/",
        views.quotation_item_empty_row,
        name="quotation_item_empty_row",
    ),


    # =========================================
    # PRODUCT STATE
    # =========================================

    path(
        "product/<int:product_id>/state/",
        views.product_state,
        name="product_state",
    ),


    # =========================================
    # QUOTATION DETAIL
    # =========================================

    path(
        "<int:pk>/detail/",
        views.quotation_detail,
        name="quotation_detail",
    ),


    # =========================================
    # UPDATE QUOTATION
    # =========================================

    path(
        "<int:pk>/edit/",
        views.quotation_update,
        name="quotation_update",
    ),


    # =========================================
    # DELETE QUOTATION
    # =========================================

    path(
        "<int:pk>/delete/",
        views.quotation_delete,
        name="quotation_delete",
    ),


    # =========================================
    # DOWNLOAD QUOTATION PDF
    # =========================================

    path(
        "<int:pk>/download/",
        views.download_quotation_pdf,
        name="download_quotation_pdf",
    ),

]