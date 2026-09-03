from datetime import date
from decimal import Decimal

from django.test import TestCase

from customers.models import Customer
from expenses.models import Expense, ExpenseCategory
from invoices.models import Invoice
from projects.models import Project, ProjectExpense
from purchases.models import Purchase, PurchaseAdditionalCost, PurchasePayment
from receipts.models import Receipt
from sales.models import Sale, SalePayment
from suppliers.models import Supplier
from vouchers.models import Voucher

from .financials import chart_data
from .services import financial_years, monthly_expenses, monthly_income


class FinancialDashboardTests(TestCase):
    def setUp(self):
        self.year = 2026
        self.january = date(self.year, 1, 15)
        self.customer = Customer.objects.create(customer_name="Cashflow Customer")

    def test_cashflow_sources_are_complete_without_double_counting(self):
        invoice = Invoice.objects.create(
            customer=self.customer,
            invoice_date=self.january,
            total_amount=Decimal("100.00"),
            balance=Decimal("100.00"),
        )
        receipt = Receipt.objects.create(
            invoice=invoice,
            receipt_date=self.january,
            amount=Decimal("100.00"),
            payment_method="cash",
        )

        direct_sale = Sale.objects.create(
            customer=self.customer,
            sale_date=self.january,
            total_amount=Decimal("50.00"),
            status="confirmed",
        )
        SalePayment.objects.create(
            sale=direct_sale,
            payment_date=self.january,
            amount=Decimal("50.00"),
            payment_method="cash",
        )

        generated_sale = Sale.objects.create(
            customer=self.customer,
            source_invoice=invoice,
            sale_date=self.january,
            total_amount=Decimal("100.00"),
            status="confirmed",
        )
        SalePayment.objects.create(
            sale=generated_sale,
            payment_date=self.january,
            amount=Decimal("100.00"),
            payment_method="cash",
            reference_number=receipt.receipt_number,
        )

        supplier = Supplier.objects.create(supplier_name="Overseas Supplier")
        purchase = Purchase.objects.create(
            supplier=supplier,
            purchase_date=self.january,
            currency="USD",
            exchange_rate=Decimal("2500.00"),
            total_amount=Decimal("10.00"),
            total_amount_tzs=Decimal("25000.00"),
        )
        PurchasePayment.objects.create(
            purchase=purchase,
            payment_date=self.january,
            amount=Decimal("10.00"),
            payment_method="bank",
        )
        PurchaseAdditionalCost.objects.create(
            purchase=purchase,
            cost_type="shipping_local",
            amount=Decimal("2000.00"),
            currency="TZS",
            payment_status="paid",
        )

        Voucher.objects.create(
            voucher_date=self.january,
            payee_name="Paid Voucher",
            approved_by="Manager",
            received_by="Payee",
            total_amount=Decimal("3000.00"),
            status="paid",
        )
        Voucher.objects.create(
            voucher_date=self.january,
            payee_name="Draft Voucher",
            approved_by="Manager",
            received_by="Payee",
            total_amount=Decimal("4000.00"),
            status="draft",
        )

        project = Project.objects.create(project_name="Cashflow Project")
        ProjectExpense.objects.create(
            project=project,
            description="Project transport",
            quantity=Decimal("1.00"),
            unit_price=Decimal("5000.00"),
            expense_date=self.january,
        )
        Expense.objects.create(
            expense_date=self.january,
            category=ExpenseCategory.objects.get(name="Operations"),
            payee=self.customer,
            description="Office expense",
            amount=Decimal("6000.00"),
            payment_method="cash",
        )

        income = monthly_income(self.year)
        expenses = monthly_expenses(self.year)
        financial = chart_data(self.year)

        self.assertEqual(income[0], Decimal("150.00"))
        self.assertEqual(expenses[0], Decimal("41000.00"))
        self.assertEqual(financial["total_income"], Decimal("150.00"))
        self.assertEqual(financial["total_expenses"], Decimal("41000.00"))
        self.assertEqual(financial["total_profit"], Decimal("-40850.00"))
        self.assertIn(self.year, financial_years())
