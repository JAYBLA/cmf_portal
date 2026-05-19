# forms.py

from django import forms
from django.forms import inlineformset_factory

from .models import Purchase, PurchaseItem


# =========================================
# PURCHASE FORM
# =========================================

class PurchaseForm(forms.ModelForm):
    
    use_required_attribute = False
    
    class Meta:

        model = Purchase

        fields = [
            "supplier",            
            "supplier_invoice_number",
            "purchase_date",
            "notes",
        ]

        widgets = {

            "purchase_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )

        }


# =========================================
# PURCHASE ITEM FORM
# =========================================

class PurchaseItemForm(forms.ModelForm):

    class Meta:

        model = PurchaseItem

        fields = [
            "product",
            "quantity",
            "unit_cost",
        ]

        widgets = {

            "product": forms.Select(
                attrs={
                    "class": "form-select form-select-sm tom-select",
                    "placeholder": "Product"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Qty"
                }
            ),

            "unit_cost": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Cost"
                }
            ),

        }

# =========================================
# FORMSET
# =========================================

PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    can_delete=True
)