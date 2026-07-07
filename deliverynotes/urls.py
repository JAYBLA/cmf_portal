from django.urls import path

from . import views

app_name = "delivery_notes"


urlpatterns = [
    # =========================================
    # LIST
    # =========================================
    path(
        "",
        views.delivery_note_list,
        name="delivery_note_list",
    ),
    # =========================================
    # TABLE
    # =========================================
    path(
        "table/",
        views.delivery_note_table,
        name="delivery_note_table",
    ),
    # =========================================
    # CREATE
    # =========================================
    path(
        "create/",
        views.delivery_note_create,
        name="delivery_note_create",
    ),
    # =========================================
    # UPDATE
    # =========================================
    path(
        "update/<int:pk>/",
        views.delivery_note_update,
        name="delivery_note_update",
    ),
    # =========================================
    # QUOTATION ITEMS
    # =========================================
    path(
        "quotation/<int:quotation_id>/items/",
        views.quotation_items,
        name="quotation_items",
    ),
    # =========================================
    # DETAIL
    # =========================================
    path(
        "detail/<int:pk>/",
        views.delivery_note_detail,
        name="delivery_note_detail",
    ),
    path(
        "delete/<int:pk>/",
        views.delivery_note_delete,
        name="delivery_note_delete",
    ),
    path(
        "<int:pk>/download/",
        views.download_delivery_note_pdf,
        name="download",
    ),

]
