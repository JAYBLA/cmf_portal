from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class RoleAccessTests(TestCase):
    def setUp(self):
        self.employee = CustomUser.objects.create_user(
            username="employee",
            password="safe-password-123",
            role=CustomUser.Roles.EMPLOYEE,
        )
        self.admin = CustomUser.objects.create_user(
            username="admin",
            password="safe-password-123",
            role=CustomUser.Roles.ADMIN,
        )
        self.super_admin = CustomUser.objects.create_user(
            username="superadmin",
            password="safe-password-123",
            role=CustomUser.Roles.SUPER_ADMIN,
        )

    def test_unauthenticated_business_page_redirects_to_login(self):
        response = self.client.get(reverse("customers:customer_list"))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('customers:customer_list')}",
        )

    def test_employee_cannot_submit_a_change(self):
        self.client.force_login(self.employee)
        response = self.client.post(reverse("customers:customer_create"))
        self.assertEqual(response.status_code, 403)

    def test_employee_can_create_sales_but_not_access_products(self):
        self.client.force_login(self.employee)
        self.assertEqual(
            self.client.get(reverse("sales:sales_create")).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("products:product_list")).status_code,
            403,
        )

    def test_employee_can_access_dashboard(self):
        self.client.force_login(self.employee)
        self.assertEqual(
            self.client.get(reverse("dashboard:dashboard")).status_code,
            200,
        )

    def test_admin_can_manage_records(self):
        self.assertTrue(self.admin.can_manage_records)
        self.assertTrue(self.admin.has_role(CustomUser.Roles.EMPLOYEE))

    def test_admin_cannot_open_receipt_create_form(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("receipts:receipt_create"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_open_receipt_download_url(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("receipts:download_receipt_pdf", kwargs={"pk": 999})
        )
        # A missing receipt yields 404, proving middleware allowed the URL.
        self.assertEqual(response.status_code, 404)

    def test_super_admin_is_configured_for_django_admin(self):
        self.assertTrue(self.super_admin.is_super_admin)
        self.assertTrue(self.super_admin.is_staff)
        self.assertTrue(self.super_admin.is_superuser)
