from django import forms

from .models import *
from django.forms import inlineformset_factory


class QuotationForm(forms.ModelForm):

    class Meta:

        model = Quotation

        fields = [
            "customer",
            "quotation_date",
            "valid_until",
            "discount_amount",         
            "notes",
        ]
        widgets = {
            "customer": forms.Select(
                attrs={
                    "data-placeholder": "Select customer",
                    "class": "form-select choices-select",
                }
            ),
            "quotation_date": forms.DateInput(attrs={"type": "date"}),
            "valid_until": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class QuotationItemForm(forms.ModelForm):

    class Meta:

        model = QuotationItem

        fields = [
            "product",
            "description",
            "quantity",
            "unit_price",
        ]


QuotationItemFormSet = inlineformset_factory(
    Quotation, QuotationItem, form=QuotationItemForm, extra=1, can_delete=True
)
