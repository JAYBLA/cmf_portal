from django.urls import path

from . import views

app_name = "delivery_notes"

urlpatterns = [
    path(
        "",
        views.delivery_note_list,
        name="delivery_note_list",
    ),
    path(
        "create/",
        views.delivery_note_create,
        name="delivery_note_create",
    ),
    path(
        "<int:pk>/edit/",
        views.delivery_note_update,
        name="delivery_note_update",
    ),
    path(
        "<int:pk>/delete/",
        views.delivery_note_delete,
        name="delivery_note_delete",
    ),
    path(
        "table/",
        views.delivery_note_table,
        name="delivery_note_table",
    ),
    path(
        "<int:pk>/pdf/",
        views.download_delivery_note_pdf,
        name="download_delivery_note_pdf",
    ),
    path(
        "<int:pk>/detail/",
        views.delivery_note_detail,
        name="delivery_note_detail",
    ),
        path(
    "quotation/<int:quotation_id>/items/",
    views.quotation_items,
    name="quotation_items",
),
]
