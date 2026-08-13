from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotations", "0002_alter_quotationitem_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="quotationitem",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="quotations/items/%Y/%m/",
            ),
        ),
    ]
