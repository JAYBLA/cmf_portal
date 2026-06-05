# urls.py

from django.urls import path
from . import views

app_name = "quotations"

urlpatterns = [
    path("", views.quotation_list, name="quotation_list"),
    path("table/", views.quotation_table, name="quotation_table"),
    path("create/", views.quotation_create, name="quotation_create"),
    path("update/<int:pk>/", views.quotation_update, name="quotation_update"),
    path("delete/<int:pk>/", views.quotation_delete, name="quotation_delete"),
    path(
        "product-details/",
        views.quotation_product_details,
        name="quotation_product_details",
    ),
]
