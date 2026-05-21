from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    
    use_required_attribute = False

    class Meta:

        model = Supplier

        fields = [
            "supplier_name",
            "contact_person",
            "supplier_website",
            "phone_number",
            "email",
            "address",
            "status",
        ]

        widgets = {

            "supplier_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter supplier name"
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "placeholder": "Enter contact person"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter phone number"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter email address"
                }
            ),

            "address": forms.TextInput(
                attrs={                   
                    "placeholder": "Enter supplier address"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select tom-select",
                    "data-placeholder": "Select status"
                }
            ),
            "supplier_website": forms.URLInput(
                attrs={
                    "placeholder": "Enter supplier website URL" 
                }
            )

        }    