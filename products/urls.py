# urls.py

from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("create/", views.product_create, name="product_create"),
    path("<int:pk>/edit/", views.product_update, name="product_update"),
    path("<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("table/", views.product_table, name="product_table"),
    # =========================================
    # STOCK MOVEMENTS
    # =========================================
    path("stock-movements/", views.stock_movement_list, name="stock_movement_list"),
    path(
        "stock-movements/table/",
        views.stock_movement_table,
        name="stock_movement_table",
    ),
]
