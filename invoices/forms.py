from django import forms
from django.forms import inlineformset_factory

from customers.models import Customer
from products.models import Product

from .models import (
Invoice,
InvoiceItem,
)
from django import forms
from django.forms import inlineformset_factory

from customers.models import Customer
from products.models import Product

from .models import *
from quotations.models import *

class InvoiceForm(forms.ModelForm):

    customer_text = forms.CharField(required=True)

    class Meta:

        model = Invoice

        fields = [            
            "invoice_date",
            "due_date",
            "discount_amount",
            "status",
            "notes",
            "invoice_type",
        ]

        widgets = {
            "invoice_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select invoice date"
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select due date"
                }
            ),

            "discount_amount": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
            "invoice_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["customer_text"].widget = forms.Select(
            attrs={
                "class": "form-select choices-tags"
            }
        )

        self.fields["customer_text"].widget.choices = [
            ("", "Select Customer")
        ] + [
            (
                str(customer.id),
                customer.customer_name
            )
            for customer in Customer.objects.all()
        ]
        
        if self.instance.pk and self.instance.customer:

            self.initial["customer_text"] = str(
                self.instance.customer.id
            )


class InvoiceItemForm(forms.ModelForm):


    class Meta:

        model = InvoiceItem

        fields = [
            "product",
            "description",
            "quantity",
            "unit_price",
        ]

        widgets = {

            "product": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Custom description"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control text-end form-control-sm",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control text-end form-control-sm",
                    "step": "0.01",
                    "min": "0"
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["product"].empty_label = (
            "Select Product"
        )

        if "DELETE" in self.fields:

            self.fields["DELETE"].widget.attrs.update(
                {
                    "class": "form-check-input"
                }
            )


InvoiceItemFormSet = inlineformset_factory(
Invoice,
InvoiceItem,
form=InvoiceItemForm,
extra=1,
can_delete=True
)
