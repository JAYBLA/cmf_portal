from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    use_required_attribute = False
    
    class Meta:
        model = Product

        fields = [
            "product_name",
            "short_description",
            "product_category",
            "sku_code",
            "product_unit",
            "product_type",
            'minimum_stock',
            "status",
        ]

        widgets = {

            "product_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter product name"
                }
            ),

            "short_description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Enter short product description"
                }
            ),

            "product_category": forms.Select(
                attrs={
                    "data-placeholder": "Select product category"
                }
            ),

            "sku_code": forms.TextInput(
                attrs={
                    "placeholder": "Enter SKU code"
                }
            ),

            "product_unit": forms.Select(
                attrs={
                    "data-placeholder": "Select product unit of measure"
                }
            ),

            "product_type": forms.Select(
                attrs={
                    "data-placeholder": "Select product type"
                }
            ),

            "status": forms.Select(
                attrs={
                    "data-placeholder": "Select status"
                }
            ),

        }    