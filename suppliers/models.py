from django.db import models


class Supplier(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    supplier_name = models.CharField(
        max_length=255
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    
    supplier_website = models.URLField(
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["supplier_name"]

    def __str__(self):

        return self.supplier_name