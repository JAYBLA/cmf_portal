from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.urls import Resolver404, resolve


class RoleAccessMiddleware:
    """Apply the portal's authentication and role policy to every request.

    Employees can view portal data. Admins can manage records except in the
    purchases and receipts modules, which are read-only for them. Super admins
    have unrestricted access, including the Django administration site.
    """

    public_prefixes = (
        "/users/login/",
        "/users/logout/",
        settings.STATIC_URL,
        settings.MEDIA_URL,
    )

    admin_read_only_views = {
        "purchases": {
            "purchase_list",
            "purchase_table",
            "detail",
            "additional_cost_list",
            "additional_cost_table",
            "additional_cost_documents",
        },
        "receipts": {
            "receipt_list",
            "receipt_table",
            "receipt_detail",
            "download_receipt_pdf",
        },
    }

    employee_allowed_views = {
        "dashboard": {"dashboard"},
        "customers": {
            "customer_list",
            "customer_table",
            "customer_detail",
        },
        "sales": {
            "sales_list",
            "sales_table",
            "sales_create",
            "sales_detail",
            "detail",
            "product_price",
        },
    }

    admin_forbidden_views = {
        ("sales", "sale_payment_create"),
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(self.public_prefixes):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if request.path.startswith("/admin/") and not request.user.is_super_admin:
            return HttpResponseForbidden("Super administrator access is required.")

        try:
            match = resolve(request.path_info)
        except Resolver404:
            match = None

        if request.user.role == request.user.Roles.EMPLOYEE:
            allowed_views = self.employee_allowed_views.get(
                match.namespace if match else None,
                set(),
            )
            if not match or match.url_name not in allowed_views:
                return HttpResponseForbidden("This page is not available to employees.")

            if (
                request.method not in ("GET", "HEAD", "OPTIONS")
                and match.url_name != "sales_create"
            ):
                return HttpResponseForbidden("Employees can only create sales.")

            return self.get_response(request)

        if (
            not request.user.is_super_admin
            and request.user.role == request.user.Roles.ADMIN
        ):
            if match and (match.namespace, match.url_name) in self.admin_forbidden_views:
                return HttpResponseForbidden(
                    "Recording sale payments is restricted to super administrators."
                )

            if (
                match
                and match.namespace in self.admin_read_only_views
                and match.url_name not in self.admin_read_only_views[match.namespace]
            ):
                return HttpResponseForbidden(
                    "Purchases and receipts are read-only for administrators."
                )

        if request.method not in ("GET", "HEAD", "OPTIONS") and not request.user.can_manage_records:
            return HttpResponseForbidden("Administrator access is required to change records.")

        return self.get_response(request)
