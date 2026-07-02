from django import forms
from django.forms import inlineformset_factory

from .models import DeliveryNote, DeliveryNoteItem


class DeliveryNoteForm(forms.ModelForm):

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
            "status",
        ]

        widgets = {
            "quotation": forms.Select(
                attrs={
                    "class": "form-select choices",
                }
            ),
            "delivery_date": forms.DateInput(
                attrs={
                    "class": "form-control flatpickr",
                    "autocomplete": "off",
                    "placeholder": "Click to select delivery date",
                }
            ),
            "delivery_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                }
            ),
            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receiver Name",
                }
            ),
            "receiver_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receiver Phone",
                }
            ),
            "driver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Driver Name",
                }
            ),
            "vehicle_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vehicle Number",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
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

        self.fields["quotation"].empty_label = "Select Quotation"


class DeliveryNoteItemForm(forms.ModelForm):

    class Meta:
        model = DeliveryNoteItem

        fields = [
            "quotation_item",
            "quantity",
            "remarks",
        ]

        widgets = {
            "quotation_item": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "Remarks",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Only show quotation items belonging to the selected quotation
        if self.instance.pk:

            self.fields["quotation_item"].queryset = (
                self.instance.delivery_note
                .quotation
                .items
                .all()
            )

        else:

            self.fields["quotation_item"].queryset = (
                self.fields["quotation_item"]
                .queryset
                .none()
            )

        if "DELETE" in self.fields:

            self.fields["DELETE"].widget.attrs.update(
                {
                    "class": "form-check-input",
                }
            )


DeliveryNoteItemFormSet = inlineformset_factory(
    DeliveryNote,
    DeliveryNoteItem,
    form=DeliveryNoteItemForm,
    extra=0,
    can_delete=True,
)