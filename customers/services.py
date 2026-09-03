from .models import Customer


def resolve_customer(value):
    """Return a selected customer, or create/reuse one from a typed name."""
    value = str(value or "").strip()
    if not value:
        raise ValueError("A customer is required.")

    try:
        return Customer.objects.get(pk=int(value))
    except (ValueError, TypeError, Customer.DoesNotExist):
        existing = Customer.objects.filter(customer_name__iexact=value).first()
        if existing:
            return existing
        return Customer.objects.create(customer_name=value)


def configure_customer_tag_field(field, selected_customer=None, label="Select Customer"):
    """Configure a form field as the common searchable, creatable customer list."""
    from django import forms

    field.widget = forms.Select(attrs={"class": "form-select choices-tags"})
    field.widget.choices = [("", label)] + [
        (str(customer.pk), customer.customer_name)
        for customer in Customer.objects.order_by("customer_name")
    ]
    return str(selected_customer.pk) if selected_customer else None
