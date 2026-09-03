from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from invoices.models import Invoice, InvoiceItem
from users.models import CustomUser

from .models import Receipt


class ReceiptCreateTransactionTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(
            username="receipt-super-admin",
            password="safe-password-123",
            role=CustomUser.Roles.SUPER_ADMIN,
        )
        self.client.force_login(user)
        customer = Customer.objects.create(customer_name="Receipt Customer")
        self.invoice = Invoice.objects.create(
            customer=customer,
            invoice_date=date.today(),
            subtotal="100.00",
            total_amount="100.00",
            balance="100.00",
            status="unpaid",
        )
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Service without stock product",
            quantity=Decimal("1.00"),
            unit_price=Decimal("100.00"),
        )

    def test_conversion_error_renders_form_and_rolls_back_receipt(self):
        response = self.client.post(
            reverse("receipts:receipt_create"),
            {
                "invoice": self.invoice.pk,
                "receipt_date": date.today().isoformat(),
                "amount": "100.00",
                "payment_method": "cash",
                "notes": "Final payment",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "without a product")
        self.assertFalse(Receipt.objects.filter(invoice=self.invoice).exists())

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, "unpaid")
        self.assertEqual(self.invoice.amount_paid, 0)

# Create your tests here.
