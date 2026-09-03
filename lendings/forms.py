from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Lending, LendingItem


class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ("customer", "lending_date", "due_date", "purpose", "notes")
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select choices-single"}),
            "lending_date": forms.DateInput(attrs={"class": "flatpickr", "autocomplete": "off", "placeholder": "Select lending date"}),
            "due_date": forms.DateInput(attrs={"class": "flatpickr", "autocomplete": "off", "placeholder": "Select expected return date"}),
            "purpose": forms.TextInput(attrs={"placeholder": "Reason for lending"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Additional lending notes"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = self.fields["customer"].queryset.order_by("customer_name")

    def clean(self):
        cleaned_data = super().clean()
        lending_date = cleaned_data.get("lending_date")
        due_date = cleaned_data.get("due_date")
        if lending_date and due_date and due_date < lending_date:
            self.add_error("due_date", "Due date cannot be before the lending date.")
        return cleaned_data


class LendingItemForm(forms.ModelForm):
    class Meta:
        model = LendingItem
        fields = (
            "item_name",
            "asset_tag",
            "quantity",
            "returned_quantity",
            "condition_out",
            "condition_return",
            "notes",
        )
        widgets = {
            "item_name": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Item or asset name"}),
            "asset_tag": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Optional asset tag"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 1}),
            "returned_quantity": forms.NumberInput(attrs={"class": "form-control form-control-sm", "min": 0}),
            "condition_out": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "condition_return": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "notes": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Optional notes"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial["quantity"] = None
            self.initial["returned_quantity"] = None
            self.initial["condition_out"] = ""
        if "condition_out" in self.fields:
            self.fields["condition_out"].choices = [("", "Select condition")] + list(
                LendingItem.Condition.choices
            )
        if "returned_quantity" in self.fields:
            self.fields["returned_quantity"].required = False
        if "condition_return" in self.fields:
            self.fields["condition_return"].required = False
            self.fields["condition_return"].choices = [("", "Not returned")] + list(
                LendingItem.Condition.choices
            )

    def clean_returned_quantity(self):
        return self.cleaned_data.get("returned_quantity") or 0

class LendingInlineItemForm(LendingItemForm):
    class Meta(LendingItemForm.Meta):
        fields = ("item_name", "quantity", "returned_quantity", "condition_out", "condition_return")


class RequiredLendingItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        has_item = any(
            form.cleaned_data
            and not form.cleaned_data.get("DELETE", False)
            and form.cleaned_data.get("item_name")
            for form in self.forms
        )
        if not has_item:
            raise ValidationError("Add at least one item to the lending.")


LendingItemFormSet = inlineformset_factory(
    Lending,
    LendingItem,
    form=LendingInlineItemForm,
    formset=RequiredLendingItemFormSet,
    fields=("item_name", "quantity", "returned_quantity", "condition_out", "condition_return"),
    extra=0,
    can_delete=True,
)


class LendingItemAddForm(LendingItemForm):
    class Meta(LendingItemForm.Meta):
        fields = ("item_name", "quantity", "condition_out")


LendingItemAddFormSet = inlineformset_factory(
    Lending,
    LendingItem,
    form=LendingItemAddForm,
    fields=("item_name", "quantity", "condition_out"),
    extra=0,
    can_delete=False,
)
