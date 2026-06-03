from django import forms
from django.forms import inlineformset_factory
from .models import *


# =========================================
# PURCHASE FORM
# =========================================

class PurchaseForm(forms.ModelForm):
    
    use_required_attribute = False
    
    class Meta:

        model = Purchase

        fields = [
            "supplier",
            "purchase_category",
            "currency",
            "exchange_rate",
            "international_shipping_cost",
            "local_shipping_cost",
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
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # DEFAULTS FOR NEW PURCHASES

        if not self.instance.pk:

            self.fields[
                "purchase_category"
            ].initial = "international"

            self.fields[
                "currency"
            ].initial = "USD"

            self.fields[
                "exchange_rate"
            ].initial = 1


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

# =========================================
# PURCHASE PAYMENT FORM
# =========================================

class PurchasePaymentForm(forms.ModelForm):

    class Meta:

        model = PurchasePayment

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
# PURCHASE ADDITIONAL COST FORM
# =========================================

class PurchaseAdditionalCostForm(forms.ModelForm):

    class Meta:

        model = PurchaseAdditionalCost

        fields = [

            "cost_type",

            "clearing_agent",

            "description",

            "amount",

            "currency",

            "exchange_rate",

            "payment_status",

            "notes",

        ]

        widgets = {

            "notes": forms.Textarea(
                attrs={
                    "rows": 2
                }
            ),

        }

    # =====================================
    # VALIDATION
    # =====================================

    def clean(self):

        cleaned_data = super().clean()

        currency = cleaned_data.get(
            "currency"
        )

        exchange_rate = cleaned_data.get(
            "exchange_rate"
        )

        amount = cleaned_data.get(
            "amount"
        )

        # =====================================
        # AMOUNT VALIDATION
        # =====================================

        if amount is not None:

            if amount <= 0:

                self.add_error(

                    "amount",

                    "Amount must be greater than zero."

                )

        # =====================================
        # TZS
        # =====================================

        if currency == "TZS":

            cleaned_data["exchange_rate"] = 1

        # =====================================
        # USD
        # =====================================

        if currency == "USD":

            if not exchange_rate or exchange_rate <= 0:

                self.add_error(

                    "exchange_rate",

                    "Exchange rate must be greater than zero."

                )

        return cleaned_data



# =========================================
# ADDITIONAL COST DOCUMENT FORM
# =========================================

class AdditionalCostDocumentForm(forms.ModelForm):

    class Meta:

        model = AdditionalCostDocument

        fields = [

            "title",

            "file"

        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder":
                        "Document title"
                }
            ),

        }

    # =====================================
    # FILE VALIDATION
    # =====================================

    def clean_file(self):

        file = self.cleaned_data.get(
            "file"
        )

        if not file:

            return file

        # =====================================
        # MAX FILE SIZE (10MB)
        # =====================================

        max_size = 10 * 1024 * 1024

        if file.size > max_size:

            raise forms.ValidationError(

                "File size must not exceed 10MB."

            )

        # =====================================
        # ALLOWED FILE TYPES
        # =====================================

        allowed_extensions = [

            ".pdf",

            ".jpg",

            ".jpeg",

            ".png",

            ".doc",

            ".docx",

            ".xls",

            ".xlsx",

        ]

        import os

        extension = os.path.splitext(
            file.name
        )[1].lower()

        if extension not in allowed_extensions:

            raise forms.ValidationError(

                (
                    "Unsupported file type. "
                    "Allowed types are: "
                    "PDF, JPG, PNG, DOC, DOCX, XLS, XLSX."
                )

            )

        return file



# =========================================
# DOCUMENT INLINE FORMSET
# =========================================

AdditionalCostDocumentFormSet = inlineformset_factory(

    PurchaseAdditionalCost,

    AdditionalCostDocument,

    form=AdditionalCostDocumentForm,

    extra=1,

    can_delete=True

)