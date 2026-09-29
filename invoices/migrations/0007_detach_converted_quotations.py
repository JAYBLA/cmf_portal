from django.db import migrations


def detach_converted_quotations(apps, schema_editor):
    Invoice = apps.get_model("invoices", "Invoice")
    Quotation = apps.get_model("quotations", "Quotation")
    alias = schema_editor.connection.alias
    converted = Invoice.objects.using(alias).exclude(invoice_type="proforma").filter(
        quotation_id__isnull=False,
    )
    Quotation.objects.using(alias).filter(
        pk__in=converted.values_list("quotation_id", flat=True),
    ).update(proforma_sync_ended=True)
    converted.update(quotation_id=None)


class Migration(migrations.Migration):
    dependencies = [
        ("invoices", "0006_invoice_quotation"),
        ("quotations", "0004_quotation_proforma_sync_ended"),
    ]

    operations = [
        migrations.RunPython(detach_converted_quotations, migrations.RunPython.noop),
    ]
