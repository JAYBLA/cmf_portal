from django import forms
from django.db.models import Q

from .models import Expense, ExpenseCategory


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "expense_date",
            "category",
            "title",
            "amount",
            "payment_method",
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
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of the expense"}
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
            "supporting_document": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.jpg,.jpeg,.png,.webp",
                }
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Expense description"}
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
