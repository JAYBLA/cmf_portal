from django.db import migrations


def snapshot_details(apps, schema_editor):
    Invoice = apps.get_model("invoices", "Invoice")
    alias = schema_editor.connection.alias
    for invoice in Invoice.objects.using(alias).filter(quotation_id__isnull=False, invoice_type="proforma"):
        quotation = invoice.quotation
        invoice.terms_conditions = "\n".join(quotation.payment_terms.values_list("term", flat=True))
        invoice.save(update_fields=["terms_conditions"])
        source_items = list(quotation.items.order_by("pk"))
        target_items = list(invoice.items.order_by("pk"))
        fields = ("product_id", "description", "quantity", "unit_price")
        if len(source_items) == len(target_items) and all(
            all(getattr(source, field) == getattr(target, field) for field in fields)
            for source, target in zip(source_items, target_items)
        ):
            for source, target in zip(source_items, target_items):
                target.image = source.image.name
                target.save(update_fields=["image"])


class Migration(migrations.Migration):
    dependencies = [("invoices", "0008_invoice_terms_conditions_invoiceitem_image")]
    operations = [migrations.RunPython(snapshot_details, migrations.RunPython.noop)]
