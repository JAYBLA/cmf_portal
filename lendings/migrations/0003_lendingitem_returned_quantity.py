from django.db import migrations, models


def copy_returned_values(apps, schema_editor):
    LendingItem = apps.get_model("lendings", "LendingItem")
    for item in LendingItem.objects.all().iterator():
        item.returned_quantity = item.quantity if item.returned else 0
        item.save(update_fields=("returned_quantity",))


class Migration(migrations.Migration):
    dependencies = [("lendings", "0002_lendingitem_returned")]
    operations = [
        migrations.AddField(
            model_name="lendingitem",
            name="returned_quantity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(copy_returned_values, migrations.RunPython.noop),
        migrations.RemoveField(model_name="lendingitem", name="returned"),
    ]
