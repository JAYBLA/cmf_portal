from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("lendings", "0001_initial")]
    operations = [
        migrations.RemoveField(model_name="lendingitem", name="returned_quantity"),
        migrations.AddField(
            model_name="lendingitem",
            name="returned",
            field=models.BooleanField(default=False),
        ),
    ]
