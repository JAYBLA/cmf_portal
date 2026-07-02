from django import forms
from django.forms import inlineformset_factory

from .models import (
    PaymentTerm,
    Quotation,
    QuotationItem,
)


# =========================================
# QUOTATION FORM
# =========================================

class QuotationForm(forms.ModelForm):

    use_required_attribute = False

    payment_terms = forms.ModelMultipleChoiceField(
        queryset=PaymentTerm.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:

        model = Quotation

        fields = [
            "title",
            "customer",
            "quote_date",
            "due_date",
            "description",
            "additional_terms",
            "payment_terms",
            "completion_period_from",
            "completion_period_to",
            "completion_period_unit",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Quotation Title",
                }
            ),

            "customer": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                }
            ),

            "quote_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "placeholder": "Select quotation date",
                    "autocomplete": "off",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "placeholder": "Select due date",
                    "autocomplete": "off",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "additional_terms": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "completion_period_from": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "completion_period_to": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "completion_period_unit": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["customer"].empty_label = "Select Customer"

        # Pre-select default payment terms on new quotations
        if not self.instance.pk:

            self.fields["payment_terms"].initial = (
                PaymentTerm.objects.filter(
                    is_default=True
                ).values_list("pk", flat=True)
            )


# =========================================
# QUOTATION ITEM FORM
# =========================================

class QuotationItemForm(forms.ModelForm):

    use_required_attribute = False

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
                    "placeholder": "Item Name",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "placeholder": "Qty",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "placeholder": "Unit Price",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if "DELETE" in self.fields:

            self.fields["DELETE"].widget.attrs.update(
                {
                    "class": "form-check-input",
                }
            )


# =========================================
# QUOTATION ITEM FORMSET
# =========================================

QuotationItemFormSet = inlineformset_factory(
    parent_model=Quotation,
    model=QuotationItem,
    form=QuotationItemForm,
    extra=0,
    can_delete=True,
)