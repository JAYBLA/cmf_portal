from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0003_remove_expense_payee"),
    ]

    operations = [
        migrations.RenameField(
            model_name="expense",
            old_name="description",
            new_name="title",
        ),
        migrations.RemoveField(
            model_name="expense",
            name="reference_number",
        ),
    ]
