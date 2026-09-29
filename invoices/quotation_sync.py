from decimal import Decimal

from django.db import transaction

from quotations.models import Quotation
from .models import Invoice, InvoiceItem


@transaction.atomic
def sync_quotation_proforma(quotation):
    """Synchronize after the quotation, its items, and its terms are saved."""
    quotation = Quotation.objects.select_for_update().get(pk=quotation.pk)
    if quotation.proforma_sync_ended:
        return None
    invoice = Invoice.objects.select_for_update().filter(quotation=quotation).first()
    # Receipts convert proformas to invoices; preserve those financial records.
    if invoice and (invoice.invoice_type != "proforma" or invoice.receipts.exists()):
        return invoice

    if invoice is None:
        invoice = Invoice(quotation=quotation, invoice_type="proforma")

    invoice.customer_id = quotation.customer_id
    invoice.title = quotation.title
    invoice.invoice_date = quotation.quote_date
    invoice.due_date = quotation.due_date
    notes = [quotation.description] if quotation.description else []
    if quotation.completion_period_from or quotation.completion_period_to:
        notes.append(
            f"Completion period: {quotation.completion_period_from}–"
            f"{quotation.completion_period_to} {quotation.get_completion_period_unit_display().lower()}"
        )
    terms = list(quotation.payment_terms.values_list("term", flat=True))
    invoice.terms_conditions = "\n".join(terms)
    if terms:
        notes.append("Payment terms:\n" + "\n".join(terms))
    invoice.notes = "\n\n".join(notes)
    items = list(quotation.items.all())
    invoice.subtotal = sum((item.total for item in items), Decimal("0.00"))
    invoice.discount_amount = Decimal("0.00")
    invoice.total_amount = invoice.subtotal
    invoice.amount_paid = Decimal("0.00")
    invoice.balance = invoice.total_amount
    invoice.status = "unpaid" if invoice.total_amount > 0 else "draft"
    invoice.save()
    invoice.items.all().delete()
    InvoiceItem.objects.bulk_create([
        InvoiceItem(
            invoice=invoice, product_id=item.product_id,
            description=item.description, quantity=item.quantity,
            image=item.image.name,
            unit_price=item.unit_price, subtotal=item.total,
        )
        for item in items
    ])
    return invoice
