import tempfile
from datetime import date
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from customers.models import Customer
from invoices.models import Invoice
from invoices.quotation_sync import sync_quotation_proforma
from users.models import CustomUser

from .models import PaymentTerm, Quotation, QuotationItem


class QuotationCopyTests(TestCase):
    def setUp(self):
        self.client.force_login(CustomUser.objects.create_user(
            username="copy-admin", password="test-password", role=CustomUser.Roles.ADMIN,
        ))
        self.customer = Customer.objects.create(customer_name="Original customer")
        self.target = Customer.objects.create(customer_name="New customer")
        self.source = Quotation.objects.create(
            customer=self.customer, title="Installation", description="Scope of work",
            quote_date=date(2026, 1, 1), due_date=date(2026, 1, 15),
            completion_period_from=2, completion_period_to=3, completion_period_unit="weeks",
        )
        self.source.payment_terms.add(PaymentTerm.objects.create(term="50% deposit"))
        self.item = QuotationItem.objects.create(
            quotation=self.source, description="Custom equipment", quantity=3,
            unit_price="125.50", image="quotations/items/example.jpg",
        )
        QuotationItem.objects.create(
            quotation=self.source, description="Labour", quantity=1,
            unit_price="50.00", is_tangible=False,
        )
        self.url = reverse("quotations:quotation_copy", args=[self.source.pk])
        self.data = {
            "customer": self.target.pk, "title": "New installation",
            "quote_date": "2026-09-29", "due_date": "2026-10-13",
        }

    def test_get_is_read_only_and_defaults_to_fresh_dates(self):
        with patch("quotations.views.timezone.localdate", return_value=date(2026, 9, 29)):
            response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertContains(response, 'hx-target="#modal-body"')
        self.assertContains(response, 'value="2026-10-13"')
        self.assertEqual(Quotation.objects.count(), 1)
        self.assertNotIn(self.customer, response.context["form"].fields["customer"].queryset)

    def test_copy_preserves_content_and_creates_independent_items(self):
        from deliverynotes.models import DeliveryNote, DeliveryNoteItem
        note = DeliveryNote.objects.create(quotation=self.source, delivery_date=date(2026, 1, 2))
        DeliveryNoteItem.objects.create(delivery_note=note, quotation_item=self.item, quantity=3)
        response = self.client.post(self.url, self.data, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Reswap"], "none")
        self.assertIn("refreshTable", response.headers["HX-Trigger"])
        copied = Quotation.objects.exclude(pk=self.source.pk).get()
        self.assertEqual(copied.associated_invoice.invoice_type, "proforma")
        self.assertEqual(copied.associated_invoice.customer, self.target)
        self.assertEqual(copied.associated_invoice.total_amount, copied.total_amount)
        self.assertEqual(copied.associated_invoice.items.count(), 2)
        self.assertEqual(copied.associated_invoice.terms_conditions, "50% deposit")
        self.assertEqual(copied.associated_invoice.items.order_by("pk").first().image.name, self.item.image.name)
        self.assertEqual(copied.customer, self.target)
        self.assertEqual(copied.description, self.source.description)
        self.assertEqual(copied.completion_period_to, 3)
        self.assertEqual(list(copied.payment_terms.all()), list(self.source.payment_terms.all()))
        fields = ("product_id", "description", "quantity", "unit_price", "image", "is_tangible")
        self.assertEqual(list(copied.items.values_list(*fields)), list(self.source.items.values_list(*fields)))
        self.assertEqual(copied.delivery_status, "Pending")
        self.assertEqual(copied.delivered_quantity, 0)
        copied.items.update(quantity=10)
        self.item.refresh_from_db()
        self.source.refresh_from_db()
        self.assertEqual(self.item.quantity, 3)
        self.assertEqual(self.source.customer, self.customer)
        self.assertEqual(self.source.delivery_status, "Completed")

    def test_invalid_customer_or_dates_does_not_create_records(self):
        for changes in ({"customer": ""}, {"customer": self.customer.pk}, {"customer": 99999}, {"due_date": "2026-09-01"}):
            response = self.client.post(self.url, {**self.data, **changes}, HTTP_HX_REQUEST="true")
            self.assertTrue(response.context["form"].errors)
            self.assertNotIn("HX-Trigger", response.headers)
            self.assertEqual(Quotation.objects.count(), 1)

    def test_item_failure_rolls_back_copy(self):
        with patch("quotations.views.QuotationItem.objects.bulk_create", side_effect=RuntimeError("Failed")):
            with self.assertRaises(RuntimeError):
                self.client.post(self.url, self.data)
        self.assertEqual(Quotation.objects.count(), 1)

    def test_missing_source_returns_404(self):
        response = self.client.get(reverse("quotations:quotation_copy", args=[99999]))
        self.assertEqual(response.status_code, 404)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class QuotationCreateHtmxTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="quotation-test-admin",
            password="test-password",
            role=CustomUser.Roles.ADMIN,
        )
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(customer_name="Test Customer")
        self.url = reverse("quotations:quotation_create")

    def tearDown(self):
        for item in Quotation.objects.prefetch_related("items"):
            for quotation_item in item.items.all():
                if quotation_item.image:
                    quotation_item.image.delete(save=False)

    def test_invalid_submission_returns_form_for_modal_swap(self):
        response = self.client.post(
            self.url,
            {
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Save Quotation")
        self.assertContains(response, "Please select or enter a customer")
        self.assertNotIn("HX-Reswap", response.headers)

    def test_successful_submission_closes_without_swapping_modal(self):
        response = self.client.post(
            self.url,
            {
                "customer_text": str(self.customer.pk),
                "title": "Working quotation",
                "quote_date": "2026-08-12",
                "due_date": "2026-08-19",
                "completion_period_from": "1",
                "completion_period_to": "2",
                "completion_period_unit": "weeks",
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-description": "Custom item",
                "items-0-quantity": "2",
                "items-0-unit_price": "1500",
                "items-0-is_tangible": "True",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Reswap"], "none")
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        self.assertTrue(Quotation.objects.filter(title="Working quotation").exists())
        quotation = Quotation.objects.get(title="Working quotation")
        invoice = quotation.associated_invoice
        self.assertEqual(invoice.invoice_type, "proforma")
        self.assertEqual(invoice.total_amount, 3000)
        self.assertEqual(invoice.balance, 3000)
        self.assertEqual(invoice.items.get().description, "Custom item")

    def test_submission_saves_item_photo(self):
        image = SimpleUploadedFile(
            "item.gif",
            (
                b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00"
                b"\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00\x00"
                b"\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        response = self.client.post(
            self.url,
            {
                "customer_text": str(self.customer.pk),
                "title": "Quotation with photo",
                "quote_date": "2026-08-12",
                "due_date": "2026-08-19",
                "completion_period_from": "1",
                "completion_period_to": "2",
                "completion_period_unit": "weeks",
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-description": "Photographed item",
                "items-0-image": image,
                "items-0-quantity": "1",
                "items-0-unit_price": "500",
                "items-0-is_tangible": "True",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        item = Quotation.objects.get(title="Quotation with photo").items.get()
        self.assertTrue(item.image.name.endswith("item.gif"))


class QuotationProformaSyncTests(TestCase):
    def setUp(self):
        self.client.force_login(CustomUser.objects.create_user(
            username="sync-admin", password="test-password", role=CustomUser.Roles.ADMIN,
        ))
        self.customer = Customer.objects.create(customer_name="Quotation customer")
        self.target = Customer.objects.create(customer_name="Updated customer")
        self.quotation = Quotation.objects.create(
            customer=self.customer, title="Original", quote_date=date(2026, 9, 1),
            due_date=date(2026, 9, 8),
        )
        self.item = self.quotation.items.create(description="Old item", quantity=2, unit_price=10)
        self.invoice = sync_quotation_proforma(self.quotation)
        self.term = PaymentTerm.objects.create(term="Payment on delivery")
        self.url = reverse("quotations:quotation_update", args=[self.quotation.pk])
        self.data = {
            "customer_text": self.target.pk, "title": "Updated quote",
            "description": "Updated scope", "quote_date": "2026-09-29", "due_date": "2026-10-06",
            "completion_period_from": "1", "completion_period_to": "3",
            "completion_period_unit": "weeks", "payment_terms": [self.term.pk],
            "items-TOTAL_FORMS": "2", "items-INITIAL_FORMS": "1",
            "items-MIN_NUM_FORMS": "0", "items-MAX_NUM_FORMS": "1000",
            "items-0-id": self.item.pk, "items-0-description": "Old item",
            "items-0-quantity": "2", "items-0-unit_price": "10",
            "items-0-is_tangible": "True", "items-0-DELETE": "on",
            "items-1-description": "Replacement item", "items-1-quantity": "4",
            "items-1-unit_price": "25.50", "items-1-is_tangible": "False",
        }

    def test_edit_updates_same_proforma_and_replaces_removed_items(self):
        for _ in range(2):
            # The second save modifies the surviving line, without adding duplicates.
            response = self.client.post(self.url, self.data, HTTP_HX_REQUEST="true")
            self.assertIn("recordSaved", response.headers["HX-Trigger"])
            self.invoice.refresh_from_db()
            self.assertEqual(Invoice.objects.count(), 1)
            self.assertEqual(self.invoice.customer, self.target)
            self.assertEqual(self.invoice.title, "Updated quote")
            self.assertEqual(self.invoice.invoice_date, date(2026, 9, 29))
            self.assertEqual(self.invoice.due_date, date(2026, 10, 6))
            self.assertEqual(self.invoice.total_amount, 102)
            self.assertEqual(self.invoice.balance, 102)
            self.assertEqual(self.invoice.items.get().description, "Replacement item")
            self.assertIn("Updated scope", self.invoice.notes)
            self.assertIn("Payment on delivery", self.invoice.notes)
            self.assertEqual(self.invoice.terms_conditions, "Payment on delivery")
            self.assertIn("1–3 weeks", self.invoice.notes)
            surviving = self.quotation.items.get()
            self.data.update({
                "items-TOTAL_FORMS": "1", "items-0-id": surviving.pk,
                "items-0-description": "Replacement item", "items-0-quantity": "4",
                "items-0-unit_price": "25.50", "items-0-is_tangible": "False",
            })
            self.data.pop("items-0-DELETE", None)

    def test_invalid_edit_leaves_proforma_unchanged(self):
        response = self.client.post(self.url, {**self.data, "title": ""})
        self.assertNotIn("HX-Trigger", response.headers)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.total_amount, 20)
        self.assertEqual(self.invoice.items.get().description, "Old item")

    def test_sync_failure_rolls_back_quotation_and_invoice(self):
        with patch("invoices.quotation_sync.InvoiceItem.objects.bulk_create", side_effect=RuntimeError("Failed")):
            with self.assertRaises(RuntimeError):
                self.client.post(self.url, self.data)
        self.quotation.refresh_from_db()
        self.invoice.refresh_from_db()
        self.assertEqual(self.quotation.title, "Original")
        self.assertEqual(self.quotation.items.get().pk, self.item.pk)
        self.assertEqual(self.invoice.items.get().description, "Old item")
        self.assertEqual(self.invoice.total_amount, 20)

    def test_edit_of_older_quotation_creates_missing_proforma(self):
        self.invoice.delete()
        response = self.client.post(self.url, self.data)
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        self.assertEqual(self.quotation.associated_invoice.total_amount, 102)

    def test_converted_invoice_is_not_overwritten(self):
        self.invoice.invoice_type = "invoice"
        self.invoice.save()
        response = self.client.post(self.url, self.data)
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.invoice_type, "invoice")
        self.assertEqual(self.invoice.title, "Original")
        self.assertEqual(self.invoice.total_amount, 20)
        self.assertIsNone(self.invoice.quotation_id)
        self.quotation.refresh_from_db()
        self.assertTrue(self.quotation.proforma_sync_ended)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertIsNone(sync_quotation_proforma(self.quotation))

    def test_payment_conversion_ends_binding_and_copy_starts_new_binding(self):
        from receipts.models import Receipt
        Receipt.objects.create(
            invoice=self.invoice, receipt_date=date(2026, 9, 29), amount=5,
        )
        self.invoice.update_payment_status()
        self.invoice.refresh_from_db()
        self.quotation.refresh_from_db()
        self.assertEqual(self.invoice.invoice_type, "invoice")
        self.assertIsNone(self.invoice.quotation_id)
        self.assertTrue(self.quotation.proforma_sync_ended)
        self.assertIsNone(sync_quotation_proforma(self.quotation))
        self.assertEqual(Invoice.objects.count(), 1)
        response = self.client.post(
            reverse("quotations:quotation_copy", args=[self.quotation.pk]),
            {"customer": self.target.pk, "title": "Fresh copy",
             "quote_date": "2026-09-29", "due_date": "2026-10-06"},
        )
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        copied = Quotation.objects.get(title="Fresh copy")
        self.assertFalse(copied.proforma_sync_ended)
        self.assertEqual(copied.associated_invoice.invoice_type, "proforma")
        self.assertEqual(Invoice.objects.count(), 2)
