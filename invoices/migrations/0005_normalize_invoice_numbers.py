from django.db import migrations


def normalize_invoice_numbers(apps, schema_editor):
    Invoice = apps.get_model("invoices", "Invoice")
    for invoice in Invoice.objects.all().only("id"):
        Invoice.objects.filter(pk=invoice.pk).update(
            invoice_number=f"CMFI00{invoice.pk}",
        )


class Migration(migrations.Migration):
    dependencies = [("invoices", "0004_alter_invoiceitem_quantity")]
    operations = [migrations.RunPython(normalize_invoice_numbers, migrations.RunPython.noop)]
