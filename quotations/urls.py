from django.urls import path

from . import views

app_name = "quotations"

urlpatterns = [
    path("", views.quotation_list, name="quotation_list"),
    path("create/", views.quotation_create, name="quotation_create"),
    path("<int:pk>/edit/", views.quotation_update, name="quotation_update"),
    path("<int:pk>/delete/", views.quotation_delete, name="quotation_delete"),
    path(
    "table/",
    views.quotation_table,
    name="quotation_table"
),
    path(
        "quotation/<int:pk>/pdf/",
        views.download_quotation_pdf,
        name="download_quotation_pdf",
    ),
    path(
        "<int:pk>/detail/",
        views.quotation_detail,
        name="quotation_detail",
    ),
]
