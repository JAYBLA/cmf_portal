from django.db import models

# =========================================
# CUSTOMER
# =========================================


class Customer(models.Model):

    STATUS = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    customer_name = models.CharField(max_length=255, unique=True)

    company_name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    phone_number = models.CharField(max_length=50, unique=True)

    email = models.EmailField(blank=True, null=True, unique=True)

    tin_number = models.CharField(max_length=100, blank=True, null=True, unique=True)

    vrn_number = models.CharField(max_length=100, blank=True, null=True, unique=True)

    address = models.TextField(blank=True, null=True)

    credit_limit = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default="active")

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ["customer_name"]

    def __str__(self):

        return self.customer_name
