from django.db import migrations, models


def convert_legacy_roles(apps, schema_editor):
    CustomUser = apps.get_model("users", "CustomUser")
    # Existing administrators and managers retain record-management access.
    CustomUser.objects.filter(role__in=("admin", "manager")).update(role="admin")
    # Accountants retain read-only access alongside existing employees.
    CustomUser.objects.filter(role="accountant").update(role="employee")
    # A Django superuser is the portal's super administrator.
    CustomUser.objects.filter(is_superuser=True).update(role="super_admin")


class Migration(migrations.Migration):
    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.RunPython(convert_legacy_roles, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("super_admin", "Super administrator"),
                    ("admin", "Administrator"),
                    ("employee", "Employee"),
                ],
                default="employee",
                max_length=20,
            ),
        ),
    ]
