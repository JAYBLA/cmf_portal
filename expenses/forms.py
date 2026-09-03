from django import forms
from django.db.models import Q

from customers.models import Customer

from .models import Expense, ExpenseCategory


class ExpenseForm(forms.ModelForm):
    payee_text = forms.CharField(required=True)

    class Meta:
        model = Expense
        fields = [
            "expense_date",
            "category",
            "payee_text",
            "description",
            "amount",
            "payment_method",
            "reference_number",
            "supporting_document",
            "notes",
        ]
        widgets = {
            "expense_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Select expense date",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Expense description"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control text-end no-spinner",
                    "min": "0.01",
                    "step": "0.01",
                    "placeholder": "Amount",
                }
            ),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "reference_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Optional payment reference"}
            ),
            "supporting_document": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png,.webp",
                }
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Additional notes"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = ExpenseCategory.objects.filter(
            is_active=True
        ).order_by("name")
        if self.instance.pk and self.instance.category_id:
            self.fields["category"].queryset = ExpenseCategory.objects.filter(
                Q(is_active=True) | Q(pk=self.instance.category_id)
            ).order_by("name")

        self.fields["payee_text"].widget = forms.Select(
            attrs={"class": "form-select choices-tags"}
        )
        self.fields["payee_text"].widget.choices = [
            ("", "Select Payee")
        ] + [
            (str(customer.pk), customer.customer_name)
            for customer in Customer.objects.order_by("customer_name")
        ]
        if self.instance.pk and self.instance.payee_id:
            self.initial["payee_text"] = str(self.instance.payee_id)

    def clean_payee_text(self):
        value = (self.cleaned_data.get("payee_text") or "").strip()
        if not value:
            raise forms.ValidationError("Please select or enter a payee.")
        return value
