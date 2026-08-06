from django.db import migrations


def normalize_receipt_numbers(apps, schema_editor):
    Receipt = apps.get_model("receipts", "Receipt")
    for receipt in Receipt.objects.all().only("id"):
        Receipt.objects.filter(pk=receipt.pk).update(
            receipt_number=f"CMFR00{receipt.pk}",
        )


class Migration(migrations.Migration):
    dependencies = [
        ("receipts", "0002_remove_receipt_payment_reference_and_more"),
    ]
    operations = [
        migrations.RunPython(
            normalize_receipt_numbers,
            migrations.RunPython.noop,
        ),
    ]
