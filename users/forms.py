from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control h-56-px bg-neutral-50 radius-12",
            "placeholder": "Username",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control h-56-px bg-neutral-50 radius-12",
            "placeholder": "Password",
            "autocomplete": "current-password",
        })
    )
