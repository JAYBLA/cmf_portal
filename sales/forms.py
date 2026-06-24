from django import forms
from django.forms import inlineformset_factory

from .models import (
    Sale,
    SaleItem,
    SalePayment,
)


# =========================================
# SALE
# =========================================

class SaleForm(forms.ModelForm):

    class Meta:

        model = Sale

        fields = [
            "customer",
            "sale_date",
            "notes",
            "status",
        ]

        widgets = {

            "customer": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                }
            ),

            "sale_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                }
            ),
        }


# =========================================
# SALE ITEM
# =========================================

class SaleItemForm(forms.ModelForm):

    class Meta:

        model = SaleItem

        fields = [
            "product",
            "quantity",
            "unit_price",
        ]

        widgets = {

            "product": forms.Select(
                attrs={
                    "class": (
                        "form-select "                        
                        "sale-product"
                    ),
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": (
                        "form-control "
                        "text-end "
                        "item-qty"
                    ),
                    "min": "0",
                }
            ),

            "unit_price": forms.NumberInput(
                attrs={
                    "class": (
                        "form-control "
                        "text-end "
                        "item-price"
                    ),
                    "readonly": True,
                }
            ),
        }


# =========================================
# SALE ITEM FORMSET
# =========================================

SaleItemFormSet = inlineformset_factory(

    Sale,

    SaleItem,

    form=SaleItemForm,

    extra=0,

    can_delete=True,
)


# =========================================
# SALE PAYMENT
# =========================================

class SalePaymentForm(forms.ModelForm):

    class Meta:

        model = SalePayment

        fields = [
            "payment_date",
            "amount",
            "payment_method",
            "reference_number",
            "notes",
        ]

        widgets = {

            "payment_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "reference_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                }
            ),
        }