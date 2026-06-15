from django import forms
from django.forms import inlineformset_factory

from .models import (
    Quotation,
    QuotationItem
)


class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotation

        fields = [
            "title",
            "customer",
            "quote_date",
            "due_date",
            "description",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Quotation Title"
                }
            ),

            "customer": forms.Select(
                attrs={
                    "class": "form-select choices"
                }
            ),

            "quote_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select quote date"
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select due date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["customer"].empty_label = (
            "Select Customer"
        )


class QuotationItemForm(forms.ModelForm):

    class Meta:
        model = QuotationItem

        fields = [
            "item_name",
            "quantity",
            "unit_price",
        ]

        widgets = {

            "item_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Item Name"
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

        if "DELETE" in self.fields:

            self.fields["DELETE"].widget.attrs.update(
                {
                    "class": "form-check-input"
                }
            )


QuotationItemFormSet = inlineformset_factory(
    Quotation,
    QuotationItem,
    form=QuotationItemForm,
    extra=1,
    can_delete=True
)