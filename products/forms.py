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
            "minimum_stock",
            "status",
        ]

        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name",
                }
            ),
            "short_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter short product description",
                }
            ),
            "product_category": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Select product category",
                }
            ),
            "sku_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter SKU code",
                }
            ),
            "product_unit": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Select product unit",
                }
            ),
            "product_type": forms.Select(
                attrs={
                    "class": "form-select",
                    "data-placeholder": "Select product type",
                }
            ),
            "minimum_stock": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "placeholder": "0",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                    "data-placeholder": "Select status",
                }
            ),
        }

    def clean_product_name(self):

        product_name = self.cleaned_data["product_name"].strip()

        if not product_name:

            raise forms.ValidationError("Product name is required.")

        return product_name

    def clean_sku_code(self):

        sku_code = self.cleaned_data["sku_code"].strip().upper()

        qs = Product.objects.filter(sku_code=sku_code)

        if self.instance.pk:

            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():

            raise forms.ValidationError("A product with this SKU already exists.")

        return sku_code

    def clean_minimum_stock(self):

        minimum_stock = self.cleaned_data.get("minimum_stock")

        if minimum_stock < 0:

            raise forms.ValidationError("Minimum stock cannot be negative.")

        return minimum_stock
