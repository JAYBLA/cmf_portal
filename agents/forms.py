from django import forms

from .models import *

# =========================================
# CLEARING AGENT FORM
# =========================================

class ClearingAgentForm(forms.ModelForm):

    class Meta:

        model = ClearingAgent

        fields = [

            "agent_name",

            "phone_number",

            "email",

            "address",

            "notes",

            "status",

        ]

        widgets = {

            "address": forms.Textarea(
                attrs={
                    "rows": 2
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 2
                }
            ),

        }
