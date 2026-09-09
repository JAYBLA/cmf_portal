from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0002_expense_categories_and_customer_payees"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expense",
            name="payee",
        ),
    ]
