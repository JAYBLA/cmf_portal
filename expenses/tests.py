import json
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from users.models import CustomUser

from .models import Expense, ExpenseCategory


class ExpenseTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="expense-admin",
            password="safe-password-123",
            role=CustomUser.Roles.ADMIN,
        )
        self.client.force_login(self.user)
        self.category = ExpenseCategory.objects.get(name="Operations")
        self.payee = Customer.objects.create(customer_name="Existing Payee")

    def test_create_expense(self):
        response = self.client.post(
            reverse("expenses:expense_create"),
            {
                "expense_date": date.today().isoformat(),
                "category": self.category.pk,
                "payee_text": "Office Supplier",
                "description": "Office supplies",
                "amount": "125000.00",
                "payment_method": "cash",
                "reference_number": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.headers["HX-Trigger"])["recordSaved"])
        expense = Expense.objects.get()
        self.assertEqual(expense.amount, Decimal("125000.00"))
        self.assertEqual(expense.expense_number, f"CMFE00{expense.pk}")
        self.assertEqual(expense.payee.customer_name, "Office Supplier")
        self.assertTrue(Customer.objects.filter(customer_name="Office Supplier").exists())

    def test_invalid_create_replaces_modal_with_errors(self):
        response = self.client.post(
            reverse("expenses:expense_create"),
            {"expense_date": date.today().isoformat(), "amount": "0"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Retarget"], "#modal-body")
        self.assertEqual(response.headers["HX-Reswap"], "innerHTML")
        self.assertContains(response, "Ensure this value is greater than or equal to")
        self.assertFalse(Expense.objects.exists())

    def test_update_and_delete_expense(self):
        expense = Expense.objects.create(
            expense_date=date.today(),
            category=self.category,
            payee=self.payee,
            description="Delivery fuel",
            amount=Decimal("50000.00"),
            payment_method="cash",
        )
        response = self.client.post(
            reverse("expenses:expense_update", kwargs={"pk": expense.pk}),
            {
                "expense_date": date.today().isoformat(),
                "category": self.category.pk,
                "payee_text": self.payee.pk,
                "description": "Delivery fuel",
                "amount": "60000.00",
                "payment_method": "cash",
                "reference_number": "",
                "notes": "Updated",
            },
        )
        self.assertEqual(response.status_code, 200)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal("60000.00"))

        response = self.client.post(
            reverse("expenses:expense_delete", kwargs={"pk": expense.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

    def test_employee_cannot_access_expenses(self):
        self.user.role = CustomUser.Roles.EMPLOYEE
        self.user.save()
        response = self.client.get(reverse("expenses:expense_list"))
        self.assertEqual(response.status_code, 403)
