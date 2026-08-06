from django.db import migrations


def normalize_voucher_numbers(apps, schema_editor):
    Voucher = apps.get_model("vouchers", "Voucher")
    for voucher in Voucher.objects.all().only("id"):
        Voucher.objects.filter(pk=voucher.pk).update(
            voucher_number=f"CMFV00{voucher.pk}",
        )


class Migration(migrations.Migration):
    dependencies = [("vouchers", "0001_initial")]
    operations = [migrations.RunPython(normalize_voucher_numbers, migrations.RunPython.noop)]
