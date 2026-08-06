from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    class Roles(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super administrator"
        ADMIN = "admin", "Administrator"
        EMPLOYEE = "employee", "Employee"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.EMPLOYEE
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # A role selected as super administrator must also work with Django's
        # built-in administration site and permission system.
        if self.role == self.Roles.SUPER_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def is_super_admin(self):
        """Whether this account has unrestricted system administration access."""
        return self.is_superuser or self.role == self.Roles.SUPER_ADMIN

    @property
    def can_manage_records(self):
        """Whether this account can create, change, or delete business records."""
        return self.is_super_admin or self.role == self.Roles.ADMIN

    def has_role(self, *roles):
        """Check a role while respecting the super-admin/admin hierarchy."""
        if self.is_super_admin:
            return True
        if self.role == self.Roles.ADMIN:
            return self.Roles.ADMIN in roles or self.Roles.EMPLOYEE in roles
        return self.Roles.EMPLOYEE in roles

    def __str__(self):
        return self.get_full_name() or self.username
