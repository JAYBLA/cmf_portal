from django import forms
from django.forms import inlineformset_factory
from .models import *
from core.widgets import IntegerDisplay

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
            "supplier_invoice_number",
            "purchase_date",
            "notes",
        ]

        widgets = {
            "supplier": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                }
            ),
            "purchase_category": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "purchase-category",
                }
            ),
            "currency": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "purchase-currency",
                }
            ),
            "exchange_rate": IntegerDisplay(
                attrs={
                    "class": "form-control no-spinner",
                    "id": "exchange-rate",
                    "step": "1",
                }
            ),
            "supplier_invoice_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "purchase_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "placeholder": "Select date",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not self.instance.pk:

            self.fields["purchase_category"].initial = "international"
            self.fields["currency"].initial = "TZS"
            self.fields["exchange_rate"].initial = 1

    def clean(self):

        cleaned_data = super().clean()

        currency = cleaned_data.get("currency")
        exchange_rate = cleaned_data.get("exchange_rate")

        if currency == "TZS":

            cleaned_data["exchange_rate"] = 1

        elif currency == "USD":

            if not exchange_rate or exchange_rate <= 0:

                self.add_error(
                    "exchange_rate", "Exchange rate must be greater than zero."
                )

        return cleaned_data


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
                    "placeholder": "Product",
                }
            ),
            "quantity": IntegerDisplay(
                attrs={"class": "form-control form-control-sm", "placeholder": "Qty","step":"1", "min":"1"}
            ),
            "unit_cost": forms.NumberInput(
                attrs={"class": "form-control form-control-sm no-spinner", "placeholder": "Cost"}
            ),
        }


# =========================================
# FORMSET
# =========================================

PurchaseItemFormSet = inlineformset_factory(
    Purchase, PurchaseItem, form=PurchaseItemForm, extra=0, can_delete=True
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
            "payment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),           
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
            "notes": forms.Textarea(attrs={"rows": 2}),            
            "exchange_rate": IntegerDisplay(attrs={"step": "1"}),
        }

    def clean(self):

        cleaned_data = super().clean()

        currency = cleaned_data.get("currency")
        exchange_rate = cleaned_data.get("exchange_rate")
        amount = cleaned_data.get("amount")

        if amount is not None and amount <= 0:

            self.add_error("amount", "Amount must be greater than zero.")

        if currency == "TZS":

            cleaned_data["exchange_rate"] = Decimal("1")

        elif currency == "USD":

            if not exchange_rate or exchange_rate <= 0:

                self.add_error(
                    "exchange_rate", "Exchange rate must be greater than zero."
                )

        return cleaned_data


# =========================================
# ADDITIONAL COST DOCUMENT FORM
# =========================================


class AdditionalCostDocumentForm(forms.ModelForm):

    class Meta:

        model = AdditionalCostDocument

        fields = ["title", "file"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Document title"}),
        }

    # =====================================
    # FILE VALIDATION
    # =====================================

    def clean_file(self):

        file = self.cleaned_data.get("file")

        if not file:

            return file

        # =====================================
        # MAX FILE SIZE (10MB)
        # =====================================

        max_size = 10 * 1024 * 1024

        if file.size > max_size:

            raise forms.ValidationError("File size must not exceed 10MB.")

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

        extension = os.path.splitext(file.name)[1].lower()

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
    extra=0,
    can_delete=True,    
)

class PurchaseProductPricingForm(forms.Form):

    purchase = forms.ModelChoiceField(
        queryset=Purchase.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select choices-select",
            }
        )
    )
