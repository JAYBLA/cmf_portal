from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path(
        "product-selling-price/",
        views.product_selling_price,
        name="product_selling_price",
    ),
]
