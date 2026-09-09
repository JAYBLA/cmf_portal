from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
        ("sales", "0004_sale_source_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="saleitem",
            name="description",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="saleitem",
            name="product",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="sale_items", to="products.product"),
        ),
    ]
