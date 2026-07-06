from django import forms
from django.forms import inlineformset_factory

from .models import *
from products.models import Product



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
    
class DeclaredPriceForm(forms.Form):

    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        empty_label="Select Product",
        label="Product",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    declared_price = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        label="Declared Price",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter declared price",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    def __init__(self, *args, pricing=None, **kwargs):

        super().__init__(*args, **kwargs)

        # =========================================
        # UPDATE MODE
        # =========================================

        if pricing is not None:

            self.fields["product"].queryset = (
                Product.objects.filter(
                    pk=pricing.product_id,
                )
            )

            self.fields["product"].initial = (
                pricing.product
            )

            self.fields["product"].disabled = True

            self.fields["declared_price"].initial = (
                pricing.declared_price
            )

        # =========================================
        # CREATE MODE
        # =========================================

        else:

            self.fields["product"].queryset = (
                Product.objects.filter(
                    sales_pricing__isnull=False,
                    sales_pricing__declared_price__isnull=True,
                )
                .order_by("product_name")
            )