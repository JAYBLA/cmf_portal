from decimal import Decimal

from django import forms
from django.db.models import Sum
from django.forms import inlineformset_factory

from .models import (
    DeliveryNote,
    DeliveryNoteItem,
)
from quotations.models import QuotationItem

# =========================================
# DELIVERY NOTE FORM
# =========================================


class DeliveryNoteForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:

        model = DeliveryNote

        fields = [
            "quotation",
            "delivery_date",
            "delivery_address",
            "receiver_name",
            "receiver_phone",
            "driver_name",
            "vehicle_number",
            "notes",
        ]

        widgets = {
            "quotation": forms.Select(
                attrs={
                    "class": "form-select choices-select",
                }
            ),
            "delivery_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Select delivery date",
                }
            ),
            "delivery_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Delivery address",
                }
            ),
            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receiver name",
                }
            ),
            "receiver_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receiver phone",
                }
            ),
            "driver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Driver name",
                }
            ),
            "vehicle_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vehicle number",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Notes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["quotation"].empty_label = "Select Quotation"


# =========================================
# DELIVERY NOTE ITEM FORM
# =========================================


class DeliveryNoteItemForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:

        model = DeliveryNoteItem

        fields = [
            "quotation_item",
            "quantity",
            "remarks",
        ]

        widgets = {
            "quotation_item": forms.HiddenInput(),
            "quantity": forms.NumberInput(
                attrs={
                    "class": ("form-control " "form-control-sm " "text-end"),
                    "step": "1",
                    "min": "1",
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": ("form-control " "form-control-sm"),
                    "placeholder": "Remarks",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.quotation_item_object = None

        # =========================================
        # EXISTING DELIVERY ITEM
        # =========================================

        if self.instance and self.instance.pk:

            self.quotation_item_object = self.instance.quotation_item

        # =========================================
        # INITIAL QUOTATION ITEM
        # =========================================

        else:

            quotation_item_id = self.initial.get("quotation_item")

            if quotation_item_id:

                try:

                    self.quotation_item_object = QuotationItem.objects.get(
                        pk=quotation_item_id
                    )

                except QuotationItem.DoesNotExist:

                    pass

    def clean(self):

        cleaned_data = super().clean()

        if cleaned_data.get("DELETE"):

            return cleaned_data

        quotation_item = cleaned_data.get("quotation_item")

        quantity = cleaned_data.get("quantity")

        if not quotation_item or quantity is None:

            return cleaned_data

        if quantity <= Decimal("0"):

            self.add_error(
                "quantity",
                ("Quantity must be " "greater than zero."),
            )

            return cleaned_data

        deliveries = quotation_item.delivery_items.all()

        if self.instance.pk:

            deliveries = deliveries.exclude(pk=self.instance.pk)

        previously_delivered = deliveries.aggregate(total=Sum("quantity"))[
            "total"
        ] or Decimal("0")

        remaining_quantity = quotation_item.quantity - previously_delivered

        if quantity > remaining_quantity:

            self.add_error(
                "quantity",
                (
                    "Delivery quantity cannot "
                    "exceed remaining quantity "
                    f"of {remaining_quantity:,.2f}."
                ),
            )

        return cleaned_data


# =========================================
# DELIVERY NOTE ITEM FORMSET
# =========================================


DeliveryNoteItemFormSet = inlineformset_factory(
    parent_model=DeliveryNote,
    model=DeliveryNoteItem,
    form=DeliveryNoteItemForm,
    extra=0,
    can_delete=True,
)
