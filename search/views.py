from django.http import JsonResponse
from django.db.models import Q

from .registry import SEARCH_MODELS


def global_search(request):

    q = request.GET.get("q", "").strip()

    results = []

    if len(q) < 2:
        return JsonResponse(results, safe=False)

    for entry in SEARCH_MODELS:

        model = entry["model"]

        query = Q()

        for field in entry["fields"]:
            query |= Q(**{f"{field}__icontains": q})

        for obj in model.objects.filter(query)[:5]:

            # Permission check goes here
            allowed_roles = entry.get("roles", [])

            if request.user.role not in allowed_roles:
                continue

            results.append({
                "title": entry["title"](obj),
                "subtitle": entry["subtitle"](obj),
                "url": entry["url"](obj),
                "icon": entry["icon"],
            })

    return JsonResponse(results, safe=False)