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
                    "placeholder": "Enter supplier name",
                }
            ),

            "contact_person": forms.TextInput(
                attrs={
                    "placeholder": "Enter contact person",
                }
            ),

            "supplier_website": forms.TextInput(
                attrs={
                    "placeholder": "e.g. example.com or www.example.com",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter phone number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter email address",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "placeholder": "Enter supplier address",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select tom-select",
                    "data-placeholder": "Select status",
                }
            ),
        }

    def clean_supplier_website(self):
        website = self.cleaned_data.get("supplier_website")

        if not website:
            return website

        website = website.strip()

        # Remove existing protocol
        if website.lower().startswith("http://"):
            website = website[7:]

        elif website.lower().startswith("https://"):
            website = website[8:]

        # Remove leading www.
        if website.lower().startswith("www."):
            website = website[4:]

        # Always store using HTTPS
        return f"https://{website}"