from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from deliverynotes.forms import DeliveryNoteForm
from invoices.forms import InvoiceForm
from projects.models import Project, ProjectExpense
from projects.forms import ProjectExpenseForm, ProjectForm
from purchases.forms import PurchaseForm, PurchasePaymentForm
from quotations.forms import QuotationForm
from receipts.forms import ReceiptForm
from sales.forms import SaleForm, SalePaymentForm
from users.models import CustomUser
from vouchers.forms import VoucherForm


class ProjectListFilterTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="project-admin",
            password="safe-password-123",
            role=CustomUser.Roles.ADMIN,
        )
        self.client.force_login(user)

        self.active_project = Project.objects.create(
            project_name="Warehouse Build",
            client_name="Alpha Client",
            status=Project.Status.ACTIVE,
            budget=Decimal("1000.00"),
            start_date=date(2026, 1, 1),
        )
        self.completed_project = Project.objects.create(
            project_name="Office Fitout",
            client_name="Beta Client",
            status=Project.Status.COMPLETED,
            budget=Decimal("500.00"),
            start_date=date(2025, 1, 1),
        )
        ProjectExpense.objects.create(
            project=self.active_project,
            expense_type=ProjectExpense.ExpenseType.MATERIAL,
            description="Cement",
            quantity=Decimal("2"),
            unit_price=Decimal("100"),
            expense_date=date(2026, 1, 2),
        )
        ProjectExpense.objects.create(
            project=self.active_project,
            expense_type=ProjectExpense.ExpenseType.LABOUR,
            description="Mason",
            quantity=Decimal("1"),
            unit_price=Decimal("50"),
            expense_date=date(2026, 1, 3),
        )
        ProjectExpense.objects.create(
            project=self.completed_project,
            expense_type=ProjectExpense.ExpenseType.LABOUR,
            description="Installer",
            quantity=Decimal("1"),
            unit_price=Decimal("80"),
            expense_date=date(2025, 1, 2),
        )

    def test_expense_category_filters_projects_and_cost(self):
        response = self.client.get(
            reverse("projects:project_table"),
            {"expense_type": ProjectExpense.ExpenseType.MATERIAL},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Warehouse Build")
        self.assertNotContains(response, "Office Fitout")
        self.assertEqual(response.context["totals"]["project_count"], 1)
        self.assertEqual(response.context["totals"]["total_cost"], Decimal("200"))
        self.assertEqual(
            response.context["projects"][0].filtered_expense_total,
            Decimal("200"),
        )

    def test_project_fields_filter_summary_totals(self):
        response = self.client.get(
            reverse("projects:project_table"),
            {
                "client_name": "beta",
                "status": Project.Status.COMPLETED,
                "budget_min": "400",
                "budget_max": "600",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Warehouse Build")
        self.assertContains(response, "Office Fitout")
        self.assertEqual(response.context["totals"]["total_budget"], Decimal("500"))
        self.assertEqual(response.context["totals"]["total_cost"], Decimal("80"))
        self.assertEqual(response.context["totals"]["total_profit"], Decimal("420"))

    def test_project_pdf_download_contains_project_and_expenses(self):
        response = self.client.get(
            reverse("projects:download_project_pdf", args=[self.active_project.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="CMFP00%s-warehouse-build-to-alpha-client.pdf"'
            % self.active_project.pk,
        )
        self.assertTrue(response.content.startswith(b"%PDF"))
        self.assertGreater(len(response.content), 1000)


class DateWidgetTests(TestCase):
    def test_all_editable_date_fields_use_flatpickr_and_placeholders(self):
        form_classes = (
            VoucherForm,
            DeliveryNoteForm,
            InvoiceForm,
            SaleForm,
            SalePaymentForm,
            ReceiptForm,
            QuotationForm,
            ProjectForm,
            ProjectExpenseForm,
            PurchaseForm,
            PurchasePaymentForm,
        )

        for form_class in form_classes:
            form = form_class()
            for field_name, field in form.fields.items():
                if not field_name.endswith("date"):
                    continue
                with self.subTest(form=form_class.__name__, field=field_name):
                    classes = field.widget.attrs.get("class", "").split()
                    self.assertIn("flatpickr", classes)
                    self.assertTrue(field.widget.attrs.get("placeholder"))
