from django.db import migrations, models
import django.db.models.deletion


CATEGORY_NAMES = {
    "operations": "Operations",
    "transport": "Transport",
    "utilities": "Utilities",
    "salaries": "Salaries and Wages",
    "marketing": "Marketing",
    "maintenance": "Repairs and Maintenance",
    "taxes": "Taxes and Fees",
    "other": "Other",
}


def migrate_expense_values(apps, schema_editor):
    Expense = apps.get_model("expenses", "Expense")
    ExpenseCategory = apps.get_model("expenses", "ExpenseCategory")
    Customer = apps.get_model("customers", "Customer")

    categories = {}
    for key, name in CATEGORY_NAMES.items():
        categories[key], _ = ExpenseCategory.objects.get_or_create(name=name)

    for expense in Expense.objects.all():
        category = categories.get(expense.category) or categories["other"]
        payee_name = (expense.payee or "Unknown Payee").strip()
        customer = Customer.objects.filter(customer_name__iexact=payee_name).first()
        if customer is None:
            customer = Customer.objects.create(customer_name=payee_name)
        expense.category_model = category
        expense.payee_customer = customer
        expense.save(update_fields=["category_model", "payee_customer"])


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0001_initial"),
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpenseCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name_plural": "Expense categories", "ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="expense",
            name="category_model",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="expenses.expensecategory"),
        ),
        migrations.AddField(
            model_name="expense",
            name="payee_customer",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="customers.customer"),
        ),
        migrations.RunPython(migrate_expense_values, migrations.RunPython.noop),
        migrations.RemoveField(model_name="expense", name="category"),
        migrations.RemoveField(model_name="expense", name="payee"),
        migrations.RenameField(model_name="expense", old_name="category_model", new_name="category"),
        migrations.RenameField(model_name="expense", old_name="payee_customer", new_name="payee"),
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="expenses.expensecategory"),
        ),
        migrations.AlterField(
            model_name="expense",
            name="payee",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="expenses", to="customers.customer"),
        ),
    ]
