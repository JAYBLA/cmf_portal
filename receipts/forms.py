from decimal import Decimal

from django import forms
from django.db.models import Sum

from .models import Receipt


# =========================================
# RECEIPT FORM
# =========================================


class ReceiptForm(forms.ModelForm):

    use_required_attribute = False


    class Meta:

        model = Receipt

        fields = [
            "invoice",
            "receipt_date",
            "amount",
            "payment_method",
            "payment_reference",
            "notes",           
        ]


        widgets = {

            "invoice": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                }
            ),


            "receipt_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Select receipt date",
                }
            ),


            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "step": "0.01",
                    "min": "0.01",
                    "placeholder": "Enter amount received",
                }
            ),


            "payment_method": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),


            "payment_reference": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Payment reference",
                }
            ),


            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Receipt Description / Notes",
                }
            ),          

        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["invoice"].empty_label = (
            "Select Invoice"
        )


    # =========================================
    # VALIDATE RECEIPT
    # =========================================

    def clean(self):

        cleaned_data = super().clean()

        invoice = cleaned_data.get("invoice")

        amount = cleaned_data.get("amount")


        if not invoice or amount is None:

            return cleaned_data


        # =====================================
        # VALIDATE POSITIVE AMOUNT
        # =====================================

        if amount <= Decimal("0.00"):

            self.add_error(
                "amount",
                "Receipt amount must be greater than zero.",
            )

            return cleaned_data


        # =====================================
        # CALCULATE EXISTING PAYMENTS
        # =====================================

        receipts = invoice.receipts.all()


        # =====================================
        # EXCLUDE CURRENT RECEIPT ON UPDATE
        # =====================================

        if self.instance.pk:

            receipts = receipts.exclude(
                pk=self.instance.pk
            )


        total_paid = (
            receipts.aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )


        # =====================================
        # CALCULATE AVAILABLE BALANCE
        # =====================================

        available_balance = (
            invoice.total_amount
            - total_paid
        )


        # =====================================
        # PREVENT OVERPAYMENT
        # =====================================

        if amount > available_balance:

            self.add_error(
                "amount",

                (
                    "Receipt amount cannot exceed "
                    f"the remaining invoice balance of "
                    f"TZS {available_balance:,.2f}."
                ),
            )


        return cleaned_data