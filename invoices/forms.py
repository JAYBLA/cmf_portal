from django import forms
from django.forms import inlineformset_factory
from products.models import Product

from .models import (
    Invoice,
    InvoiceItem
)



# =========================================
# INVOICE FORM
# =========================================

class InvoiceForm(forms.ModelForm):

    class Meta:

        model = Invoice

        fields = [

            "customer",

            "invoice_date",

            "due_date",

            "discount_amount",

            "notes",

        ]

        widgets = {

            "invoice_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "discount_amount": forms.NumberInput(
                attrs={
                    "placeholder":
                        "Invoice Discount"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 2,

                    "placeholder":
                        "Invoice notes..."
                }
            ),

        }



# =========================================
# INVOICE ITEM FORM
# =========================================

class InvoiceItemForm(forms.ModelForm):

    class Meta:

        model = InvoiceItem

        fields = [

            "product",

            "quantity",

            "unit_price",

        ]

    def __init__(

        self,

        *args,

        **kwargs

    ):

        super().__init__(

            *args,

            **kwargs

        )

        self.fields[
            "product"
        ].queryset = (

            Product.objects.filter(
                status="active"
            )

        )


# =========================================
# INVOICE ITEM FORMSET
# =========================================

InvoiceItemFormSet = inlineformset_factory(

    Invoice,

    InvoiceItem,

    form=InvoiceItemForm,

    extra=1,

    can_delete=True

)