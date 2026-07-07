from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    # =========================================
    # SALES
    # =========================================
    path(
        "",
        views.sale_list,
        name="sales_list",
    ),
    path(
        "table/",
        views.sale_table,
        name="sales_table",
    ),
    path(
        "create/",
        views.sale_create,
        name="sales_create",
    ),
    path(
        "update/<int:pk>/",
        views.sale_update,
        name="sales_update",
    ),
    path(
        "delete/<int:pk>/",
        views.sale_delete,
        name="sale_delete",
    ),
    # =========================================
    # SALE PAYMENTS
    # =========================================
    path(
        "payments/create/<int:sale_id>/",
        views.sale_payment_create,
        name="sale_payment_create",
    ),
    # =========================================
    # PRODUCT PRICE LOOKUP
    # =========================================
    path(
        "product-price/<int:product_id>/",
        views.product_price,
        name="product_price",
    ),
    path("sale/<int:pk>/detail/", views.sale_detail, name="sales_detail"),
    # =========================================
    # DECLARED PRICES
    # =========================================

    path(
        "pricing/",
        views.declared_price_list,
        name="declared_price_list",
    ),

    path(
        "pricing/table/",
        views.declared_price_table,
        name="declared_price_table",
    ),

    path(
        "pricing/create/",
        views.declared_price_create,
        name="declared_price_create",
    ),

    path(
        "pricing/<int:pk>/update/",
        views.declared_price_update,
        name="declared_price_update",
    ),

    path(
        "pricing/<int:pk>/delete/",
        views.declared_price_delete,
        name="declared_price_delete",
    ),
    path(

        "<int:pk>/detail/",

        views.sale_detail,

        name="detail",

    ),

]
