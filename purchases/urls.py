from django.urls import path

from . import views

app_name = "purchases"


urlpatterns = [
    path("", views.purchase_list, name="purchase_list"),
    path("create/", views.purchase_create, name="purchase_create"),
    path("update/<int:pk>/", views.purchase_update, name="purchase_update"),
    path("delete/<int:pk>/", views.purchase_delete, name="purchase_delete"),
    
    path("table/", views.purchase_table, name="purchase_table"),
    path(
        "<int:purchase_id>/payments/create/",
        views.purchase_payment_create,
        name="purchase_payment_create",
    ),
    path(
        "<int:pk>/detail/",
        views.purchase_detail,
        name="detail",
    ),
    # =====================================
    # PURCHASE ADDITIONAL COSTS
    # =====================================
    path(
        "<int:purchase_id>/additional-costs/",
        views.additional_cost_list,
        name="additional_cost_list",
    ),
    path(
        "<int:purchase_id>/additional-costs/create/",
        views.additional_cost_create,
        name="additional_cost_create",
    ),
    path(
        "additional-costs/<int:pk>/update/",
        views.additional_cost_update,
        name="additional_cost_update",
    ),
    path(
        "additional-costs/<int:pk>/delete/",
        views.additional_cost_delete,
        name="additional_cost_delete",
    ),
    path(
        "additional-costs/table/<int:purchase_id>/",
        views.additional_cost_table,
        name="additional_cost_table",
    ),
    path(
    "additional-costs/<int:pk>/documents/",
    views.additional_cost_documents,
    name="additional_cost_documents",
),
]
