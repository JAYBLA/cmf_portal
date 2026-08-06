from datetime import date
from decimal import Decimal

from django.test import TestCase

from customers.models import Customer
from invoices.models import Invoice, InvoiceItem
from products.models import Product, ProductCategory, ProductUnit, StockMovement
from receipts.models import Receipt
from sales.models import Sale
from sales.services.invoice_conversion import reconcile_invoice_sale


class PaidInvoiceSaleConversionTests(TestCase):
    def setUp(self):
        customer = Customer.objects.create(customer_name="Invoice Customer")
        category = ProductCategory.objects.create(name="Conversion Test Category")
        unit = ProductUnit.objects.create(name="Piece", abbreviation="pc")
        self.product = Product.objects.create(
            product_name="Conversion Test Product",
            sku_code="CONVERSION-TEST-1",
            product_category=category,
            product_unit=unit,
            current_stock=Decimal("10.00"),
        )
        self.invoice = Invoice.objects.create(
            customer=customer,
            invoice_date=date.today(),
            subtotal=Decimal("20.00"),
            total_amount=Decimal("20.00"),
            amount_paid=Decimal("20.00"),
            balance=Decimal("0.00"),
            status="paid",
        )
        InvoiceItem.objects.create(
            invoice=self.invoice,
            product=self.product,
            quantity=Decimal("2.00"),
            unit_price=Decimal("10.00"),
        )
        self.receipt = Receipt.objects.create(
            invoice=self.invoice,
            receipt_date=date.today(),
            amount=Decimal("20.00"),
            payment_method="nmb bank deposit",
            notes="Paid at NMB",
        )

    def test_paid_invoice_creates_one_sale_and_reverses_when_unpaid(self):
        sale = reconcile_invoice_sale(self.invoice)

        self.assertEqual(Sale.objects.filter(source_invoice=self.invoice).count(), 1)
        self.assertEqual(sale.status, "confirmed")
        self.assertEqual(sale.payment_status, "paid")
        self.assertEqual(sale.amount_paid, Decimal("20.00"))
        self.assertEqual(sale.balance, Decimal("0.00"))
        payment = sale.payments.get()
        self.assertEqual(payment.amount, Decimal("20.00"))
        self.assertEqual(payment.payment_method, "bank")
        self.assertEqual(payment.reference_number, self.receipt.receipt_number)
        self.product.refresh_from_db()
        self.assertEqual(self.product.current_stock, Decimal("8.00"))

        # Re-running after the same paid status is idempotent.
        reconcile_invoice_sale(self.invoice)
        self.assertEqual(StockMovement.objects.count(), 1)
        self.assertEqual(sale.payments.count(), 1)

        self.receipt.amount = Decimal("10.00")
        self.receipt.save(update_fields=["amount"])
        self.invoice.status = "partial"
        self.invoice.amount_paid = Decimal("10.00")
        self.invoice.balance = Decimal("10.00")
        self.invoice.save(update_fields=["status", "amount_paid", "balance"])
        reconcile_invoice_sale(self.invoice)

        sale.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(sale.status, "cancelled")
        self.assertEqual(sale.payment_status, "partial")
        self.assertEqual(sale.amount_paid, Decimal("10.00"))
        self.assertEqual(sale.balance, Decimal("10.00"))
        self.assertEqual(sale.payments.get().amount, Decimal("10.00"))
        self.assertEqual(self.product.current_stock, Decimal("10.00"))
        self.assertEqual(StockMovement.objects.count(), 2)
