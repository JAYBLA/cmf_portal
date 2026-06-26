from search.registry import SEARCH_MODELS
from .models import Customer

SEARCH_MODELS.append({
    "model": Customer,
    "fields": ["name", "email"],
    "roles": ["admin", "manager", "employee"],
    "title": lambda obj: obj.name,
    "subtitle": lambda obj: obj.email,
    "url": lambda obj: reverse("customers:customer_detail", args=[obj.pk]),
    "icon": "ri:user-line",
})