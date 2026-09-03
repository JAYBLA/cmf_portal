from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from users.models import CustomUser

from .forms import LendingForm, LendingItemForm, LendingItemFormSet
from .models import Lending, LendingItem


class LendingTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username="lending-admin", password="safe-password-123", role=CustomUser.Roles.ADMIN)
        self.client.force_login(user)
        self.customer = Customer.objects.create(customer_name="Borrower One")
        self.lending = Lending.objects.create(customer=self.customer, lending_date=date.today(), due_date=date.today() + timedelta(days=7))

    def test_lending_list_and_customer_are_visible(self):
        response = self.client.get(reverse("lendings:lending_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Borrower One")
        self.assertContains(response, self.lending.lending_number)

    def test_return_quantities_update_lending_status(self):
        item = LendingItem.objects.create(lending=self.lending, item_name="Laptop", quantity=2, returned_quantity=1)
        LendingItem.objects.create(lending=self.lending, item_name="Charger", quantity=1)
        self.lending.refresh_return_status()
        self.assertEqual(self.lending.return_status, Lending.ReturnStatus.PARTIAL)
        item.returned_quantity = 2
        item.save()
        self.lending.items.filter(item_name="Charger").update(returned_quantity=1)
        self.lending.refresh_return_status()
        self.assertEqual(self.lending.return_status, Lending.ReturnStatus.RETURNED)
        self.assertEqual(self.lending.returned_date, date.today())

    def test_returned_quantity_defaults_to_zero(self):
        item = LendingItem.objects.create(
            lending=self.lending,
            item_name="Chair",
            quantity=1,
        )
        self.assertEqual(item.returned_quantity, 0)
        self.assertEqual(item.outstanding_quantity, 1)

    def test_returned_quantity_cannot_exceed_quantity_lent(self):
        form = LendingItemForm(data={
            "item_name": "Chair",
            "quantity": 1,
            "returned_quantity": 2,
            "condition_out": "good",
            "condition_return": "good",
            "asset_tag": "",
            "notes": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("returned_quantity", form.errors)

    def test_auto_generated_item_row_starts_completely_blank(self):
        empty_form = LendingItemFormSet(prefix="items").empty_form

        self.assertEqual(empty_form.initial.get("condition_out"), "")
        self.assertEqual(empty_form.fields["condition_out"].choices[0][0], "")
        self.assertIsNone(empty_form.initial.get("quantity"))
        self.assertIsNone(empty_form.initial.get("returned_quantity"))

    def test_due_date_cannot_precede_lending_date(self):
        form = LendingForm(data={"customer": self.customer.pk, "lending_date": "2026-08-14", "due_date": "2026-08-13", "purpose": "Testing", "notes": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("due_date", form.errors)

    def test_add_items_endpoint_saves_multiple_arbitrary_items(self):
        response = self.client.post(
            reverse("lendings:item_create", args=[self.lending.pk]),
            {
                "items-TOTAL_FORMS": "2",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-item_name": "Laptop",
                "items-0-asset_tag": "CMF-IT-001",
                "items-0-quantity": "1",
                "items-0-condition_out": "good",
                "items-0-notes": "With charger",
                "items-1-item_name": "Folding chair",
                "items-1-asset_tag": "",
                "items-1-quantity": "4",
                "items-1-condition_out": "fair",
                "items-1-notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.lending.items.count(), 2)
        self.assertEqual(self.lending.total_quantity, 5)
        self.assertIn("recordSaved", response["HX-Trigger"])

    def test_create_lending_form_saves_header_and_items_together(self):
        response = self.client.post(
            reverse("lendings:lending_create"),
            {
                "customer": self.customer.pk,
                "lending_date": "2026-08-14",
                "due_date": "2026-08-20",
                "purpose": "Field demonstration",
                "notes": "Return after use",
                "items-TOTAL_FORMS": "2",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-item_name": "Projector",
                "items-0-asset_tag": "CMF-AV-001",
                "items-0-quantity": "1",
                "items-0-returned_quantity": "0",
                "items-0-condition_out": "good",
                "items-0-condition_return": "",
                "items-0-notes": "With remote",
                "items-1-item_name": "Extension cable",
                "items-1-asset_tag": "",
                "items-1-quantity": "2",
                "items-1-returned_quantity": "0",
                "items-1-condition_out": "good",
                "items-1-condition_return": "",
                "items-1-notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        created = Lending.objects.get(purpose="Field demonstration")
        self.assertEqual(created.items.count(), 2)
        self.assertEqual(created.total_quantity, 3)
        self.assertIn("recordSaved", response["HX-Trigger"])

    def test_create_lending_requires_at_least_one_item(self):
        initial_count = Lending.objects.count()
        response = self.client.post(
            reverse("lendings:lending_create"),
            {
                "customer": self.customer.pk,
                "lending_date": "2026-08-14",
                "due_date": "2026-08-20",
                "purpose": "No items",
                "notes": "",
                "items-TOTAL_FORMS": "0",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lending.objects.count(), initial_count)
        self.assertContains(response, "Add at least one item")
