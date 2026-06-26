from products.models import Product
from sales.models import SalesProductPricing

stock_report = (
    Product.objects
    .select_related("product_category")
    .prefetch_related("sales_pricing")
    .order_by("product_name")[:10]
)

context["stock_report"] = stock_report

