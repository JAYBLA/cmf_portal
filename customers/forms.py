from django import forms

from .models import Customer



# =========================================
# CUSTOMER FORM
# =========================================

class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = "__all__"

        widgets = {

            "customer_name": forms.TextInput(
                attrs={
                    "placeholder":
                        "Enter customer full name"
                }
            ),

            "company_name": forms.TextInput(
                attrs={
                    "placeholder":
                        "Enter company/business name"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "placeholder":
                        "e.g. +255712345678"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder":
                        "e.g. customer@email.com"
                }
            ),

            "tin_number": forms.TextInput(
                attrs={
                    "placeholder":
                        "Enter customer TIN number"
                }
            ),

            "vrn_number": forms.TextInput(
                attrs={
                    "placeholder":
                        "Enter customer VRN number"
                }
            ),

            "credit_limit": forms.NumberInput(
                attrs={
                    "placeholder":
                        "Maximum credit allowed",
                }
            ),

            "opening_balance": forms.NumberInput(
                attrs={
                    "placeholder":
                        "Existing customer debt balance",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder":
                        "Enter customer address"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder":
                        "Optional internal notes..."
                }
            ),

        }