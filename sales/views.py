from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from products.models import Product


def product_selling_price(request):

    product_id = request.GET.get("product_id")

    if not product_id:

        return JsonResponse({"selling_price": 0})

    product = get_object_or_404(Product, pk=product_id)

    return JsonResponse({"selling_price": float(product.selling_price)})
