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
]
