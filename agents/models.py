from django.db import models

class ClearingAgent(models.Model):

    agent_name = models.CharField(
        max_length=255
    )

    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("active", "Active"),
            ("inactive", "Inactive"),
        ),
        default="active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["agent_name"]

    def __str__(self):

        return self.agent_name