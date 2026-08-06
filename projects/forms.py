from django import forms
from django.forms import inlineformset_factory

from customers.models import Customer

from .models import Project, ProjectExpense


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "project_name",
            "client_name",
            "status",
            "start_date",
            "end_date",
            "budget",
            "description",
        )
        widgets = {
            "project_name": forms.TextInput(attrs={"placeholder": "Enter project name"}),
            "start_date": forms.DateInput(attrs={"class": "flatpickr", "placeholder": "Select start date"}),
            "end_date": forms.DateInput(attrs={"class": "flatpickr", "placeholder": "Select end date"}),
            "budget": forms.NumberInput(attrs={"placeholder": "0.00", "min": "0", "step": "0.01"}),
            "description": forms.Textarea(attrs={"placeholder": "Project scope or notes", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customers = Customer.objects.order_by("customer_name").values_list(
            "customer_name",
            flat=True,
        )
        choices = [("", "Select or type a customer")]
        choices.extend((name, name) for name in customers)

        current_client = self.initial.get("client_name")
        if current_client and current_client not in {value for value, _ in choices}:
            choices.append((current_client, current_client))

        self.fields["client_name"].widget = forms.Select(
            choices=choices,
            attrs={
                "class": "choices-tags",
                "data-placeholder": "Select or type a customer",
            },
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before the start date.")
        return cleaned_data


class ProjectExpenseForm(forms.ModelForm):
    class Meta:
        model = ProjectExpense
        fields = ("expense_type", "description", "quantity", "unit_price", "expense_date")
        widgets = {
            "expense_type": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "expense_date": forms.DateInput(attrs={"class": "flatpickr", "placeholder": "Today (default)"}),
            "description": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "What was purchased or paid for?"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control form-control-sm expense-quantity", "placeholder": "1", "min": "0.01", "step": "0.01"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control form-control-sm expense-unit-price", "placeholder": "0.00", "min": "0", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keep every unsaved form blank, including automatically added rows
        # in a bound formset. Otherwise model defaults make an empty row look
        # changed and Django rejects the entire submission.
        if not self.instance.pk:
            self.initial["expense_type"] = ""
            self.initial["quantity"] = None
            self.initial["unit_price"] = None
        self.fields["expense_date"].required = False
        self.fields["expense_type"].required = False

        self.fields["expense_type"].choices = [("", "Select type")] + list(
            self.fields["expense_type"].choices
        )


ProjectExpenseFormSet = inlineformset_factory(
    Project,
    ProjectExpense,
    form=ProjectExpenseForm,
    # The shared auto-formset script creates the first blank row on load.
    # Starting at zero prevents a second row being added because today's
    # prefilled date counts as entered data.
    extra=0,
    can_delete=False,
)
