from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("project_name", models.CharField(max_length=255)),
                ("client_name", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("budget", models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ("status", models.CharField(choices=[("planning", "Planning"), ("active", "Active"), ("on_hold", "On hold"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="planning", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
