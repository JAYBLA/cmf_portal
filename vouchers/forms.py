from django import forms
from django.forms import inlineformset_factory

from .models import Voucher, VoucherItem


class VoucherForm(forms.ModelForm):

    class Meta:
        model = Voucher

        fields = [
            "voucher_date",
            "payee_name",
            "payee_phone",
            "approved_by",
            "received_by",
            "notes",
            "status",
        ]

        widgets = {
            "voucher_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select voucher date",
                }
            ),
            "payee_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Payee Name",
                }
            ),
            "payee_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Payee Phone Number",
                }
            ),
            "approved_by": forms.TextInput(
                 attrs={
                    "class": "form-control",
                    "placeholder": "Approved By",
                }
            ),
            "received_by": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Received By",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Additional Notes",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["approved_by"].empty_label = "Select Approver"


class VoucherItemForm(forms.ModelForm):

    class Meta:
        model = VoucherItem

        fields = [
            "description",
            "amount",
        ]

        widgets = {
            "description": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Payment Description",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Amount",
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


VoucherItemFormSet = inlineformset_factory(
    Voucher,
    VoucherItem,
    form=VoucherItemForm,
    extra=0,
    can_delete=True,
)