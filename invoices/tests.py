from datetime import date

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from deliverynotes.models import DeliveryNote
from invoices.models import Invoice
from quotations.models import Quotation
from receipts.models import Receipt
from users.models import CustomUser
from vouchers.models import Voucher


class InvoiceModalSaveTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="invoice-admin",
            password="safe-password-123",
            role=CustomUser.Roles.ADMIN,
        )
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(customer_name="Modal Customer")
        self.url = reverse("invoices:invoice_create")

    def _post_data(self):
        return {
            "customer_text": str(self.customer.pk),
            "invoice_type": "invoice",
            "invoice_date": date.today().isoformat(),
            "due_date": "",
            "discount_amount": "0",
            "notes": "",
            "title": "Test invoice",
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            "items-0-product": "",
            "items-0-description": "Service",
            "items-0-quantity": "1",
            "items-0-unit_price": "100",
        }

    def test_valid_save_triggers_modal_close(self):
        response = self.client.post(self.url, self._post_data())

        self.assertEqual(response.status_code, 200)
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        self.assertEqual(Invoice.objects.count(), 1)

    def test_invalid_save_replaces_modal_with_visible_errors(self):
        data = self._post_data()
        data["customer_text"] = ""

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Retarget"], "#modal-body")
        self.assertEqual(response.headers["HX-Reswap"], "innerHTML")
        self.assertContains(response, "Please select or enter a customer.")
        self.assertEqual(Invoice.objects.count(), 0)


class DocumentNumberTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="Number Customer")

    def test_document_numbers_follow_quotation_syntax(self):
        invoice = Invoice.objects.create(
            customer=self.customer,
            invoice_date=date.today(),
        )
        receipt = Receipt.objects.create(
            invoice=invoice,
            receipt_date=date.today(),
            amount="100.00",
            payment_method="cash",
        )
        voucher = Voucher.objects.create(
            voucher_date=date.today(),
            payee_name="Number Payee",
            approved_by="Approver",
            received_by="Receiver",
        )
        quotation = Quotation.objects.create(
            title="Number Quotation",
            customer=self.customer,
            quote_date=date.today(),
            due_date=date.today(),
        )
        delivery_note = DeliveryNote.objects.create(
            quotation=quotation,
            delivery_date=date.today(),
        )

        self.assertEqual(invoice.invoice_number, f"CMFI00{invoice.pk}")
        self.assertEqual(receipt.receipt_number, f"CMFR00{receipt.pk}")
        self.assertEqual(voucher.voucher_number, f"CMFV00{voucher.pk}")
        self.assertEqual(
            delivery_note.delivery_number,
            f"CMFDN00{delivery_note.pk}",
        )
