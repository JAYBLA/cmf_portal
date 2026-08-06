from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("projects", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="ProjectExpense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("expense_type", models.CharField(choices=[("material", "Material"), ("labour", "Labour"), ("transport", "Transport"), ("equipment", "Equipment"), ("other", "Other")], default="material", max_length=20)),
                ("description", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("expense_date", models.DateField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="expenses", to="projects.project")),
            ],
            options={"ordering": ("-expense_date", "-id")},
        ),
    ]
