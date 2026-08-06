from decimal import Decimal

from django.db import migrations, models


def populate_unit_prices(apps, schema_editor):
    ProjectExpense = apps.get_model("projects", "ProjectExpense")
    for expense in ProjectExpense.objects.all():
        expense.quantity = Decimal("1")
        expense.unit_price = expense.amount
        expense.save(update_fields=["quantity", "unit_price"])


class Migration(migrations.Migration):
    dependencies = [("projects", "0002_projectexpense")]

    operations = [
        migrations.AddField(
            model_name="projectexpense",
            name="quantity",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12),
        ),
        migrations.AddField(
            model_name="projectexpense",
            name="unit_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.RunPython(populate_unit_prices, migrations.RunPython.noop),
        migrations.RemoveField(model_name="projectexpense", name="notes"),
        migrations.AlterField(
            model_name="projectexpense",
            name="amount",
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=14),
        ),
    ]
