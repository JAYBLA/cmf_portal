from django.db import migrations


def normalize_delivery_numbers(apps, schema_editor):
    DeliveryNote = apps.get_model("deliverynotes", "DeliveryNote")
    for delivery_note in DeliveryNote.objects.all().only("id"):
        DeliveryNote.objects.filter(pk=delivery_note.pk).update(
            delivery_number=f"CMFDN00{delivery_note.pk}",
        )


class Migration(migrations.Migration):
    dependencies = [("deliverynotes", "0004_alter_deliverynoteitem_quantity")]
    operations = [migrations.RunPython(normalize_delivery_numbers, migrations.RunPython.noop)]
