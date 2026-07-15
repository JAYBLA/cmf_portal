from django import forms

from django.forms import (
    inlineformset_factory,
)

from customers.models import Customer
from products.models import Product

from .models import (
    Quotation,
    QuotationItem,
    PaymentTerm,
)
from datetime import (
    date,
    timedelta,
)



# =========================================
# QUOTATION FORM
# =========================================


class QuotationForm(forms.ModelForm):

    customer_text = forms.CharField(
        required=False,
    )
    
    payment_terms = forms.ModelMultipleChoiceField(
        queryset=PaymentTerm.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )


    class Meta:

        model = Quotation

        fields = [
            "title",
            "description",
            "quote_date",
            "due_date",
            "completion_period_from",
            "completion_period_to",
            "completion_period_unit",
            "payment_terms",           
        ]


        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Quotation title"
                    ),
                }
            ),


            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "Quotation description"
                    ),
                }
            ),


            "quote_date": forms.DateInput(
                attrs={
                    "class": (
                        "form-control flatpickr"
                    ),
                    "autocomplete": "off",
                    "placeholder": (
                        "Select quotation date"
                    ),
                }
            ),


            "due_date": forms.DateInput(
                attrs={
                    "class": (
                        "form-control flatpickr"
                    ),
                    "autocomplete": "off",
                    "placeholder": (
                        "Select due date"
                    ),
                }
            ),


            "completion_period_from":
                forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": "0",
                    }
                ),


            "completion_period_to":
                forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": "0",
                    }
                ),


            "completion_period_unit":
                forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),
        }


    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )
        
        # =========================================
        # DEFAULT QUOTATION DATES
        # =========================================

        if not self.instance.pk:

            today = date.today()

            self.fields[
                "quote_date"
            ].initial = today

            self.fields[
                "due_date"
            ].initial = (
                today
                + timedelta(days=7)
            )



        # =========================================
        # CUSTOMER FIELD
        # =========================================

        self.fields[
            "customer_text"
        ].widget = forms.Select(
            attrs={
                "class": (
                    "form-select choices-tags"
                ),
            }
        )


        self.fields[
            "customer_text"
        ].widget.choices = [

            (
                "",
                "Select Customer",
            )

        ] + [

            (
                str(customer.id),
                customer.customer_name,
            )

            for customer in (
                Customer.objects
                .order_by("customer_name")
            )

        ]


        # =========================================
        # UPDATE CUSTOMER
        # =========================================

        if (
            self.instance
            and self.instance.pk
            and self.instance.customer_id
        ):

            self.initial[
                "customer_text"
            ] = str(
                self.instance.customer_id
            )


    # =========================================
    # VALIDATE CUSTOMER
    # =========================================

    def clean_customer_text(self):

        customer_text = (
            self.cleaned_data.get(
                "customer_text"
            )
            or ""
        ).strip()


        if not customer_text:

            raise forms.ValidationError(
                (
                    "Please select or enter "
                    "a customer."
                )
            )


        return customer_text


# =========================================
# QUOTATION ITEM FORM
# =========================================


class QuotationItemForm(forms.ModelForm):


    class Meta:

        model = QuotationItem

        fields = [
            "product",
            "description",
            "quantity",
            "unit_price",
            "is_tangible",
        ]


        widgets = {

            # =====================================
            # PRODUCT
            # =====================================

            "product": forms.Select(
                attrs={
                    "class": (
                        "form-select "
                        "form-select-sm"
                    ),
                }
            ),


            # =====================================
            # CUSTOM ITEM
            # =====================================

            "description": forms.TextInput(
                attrs={
                    "class": (
                        "form-control "
                        "form-control-sm"
                    ),
                    "placeholder": (
                        "Or type custom item"
                    ),
                }
            ),


            # =====================================
            # QUANTITY
            # =====================================

            "quantity": forms.NumberInput(
                attrs={
                    "class": (
                        "form-control "
                        "text-end "
                        "form-control-sm"
                    ),
                    "step": "1",
                    "min": "1",
                    "placeholder": "Qty",
                }
            ),


            # =====================================
            # UNIT PRICE
            # =====================================

            "unit_price": forms.NumberInput(
                attrs={
                    "class": (
                        "form-control no-spinner"
                        "text-end "
                        "form-control-sm"
                    ),
                    "step": "0.01",
                    "min": "0",
                    "placeholder": (
                        "Unit price"
                    ),
                }
            ),


            # =====================================
            # TANGIBLE
            # =====================================

            "is_tangible": forms.Select(
                choices=(
                    (True, "Yes"),
                    (False, "No"),
                ),
                attrs={
                    "class": (
                        "form-select "
                        "form-select-sm"
                    ),
                }
            ),

        }


    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )


        # =========================================
        # PRODUCT OPTIONAL
        # =========================================

        self.fields[
            "product"
        ].required = False


        self.fields[
            "product"
        ].empty_label = (
            "Select Product"
        )


        # =========================================
        # DESCRIPTION OPTIONAL
        # =========================================

        self.fields[
            "description"
        ].required = False


        # =========================================
        # ACTIVE PRODUCTS
        # =========================================

        self.fields[
            "product"
        ].queryset = (
            Product.objects
            .filter(
                status="active",
            )
            .order_by(
                "product_name",
            )
        )


        # =========================================
        # DELETE FIELD
        # =========================================

        if "DELETE" in self.fields:

            self.fields[
                "DELETE"
            ].widget.attrs.update(
                {
                    "class": (
                        "form-check-input"
                    ),
                }
            )


    # =========================================
    # VALIDATE ITEM
    # =========================================

    def clean(self):

        cleaned_data = super().clean()


        product = cleaned_data.get(
            "product"
        )


        description = (
            cleaned_data.get(
                "description"
            )
            or ""
        ).strip()


        quantity = cleaned_data.get(
            "quantity"
        )


        unit_price = cleaned_data.get(
            "unit_price"
        )


        delete = cleaned_data.get(
            "DELETE"
        )


        # =========================================
        # DELETED ROW
        # =========================================

        if delete:

            return cleaned_data


        # =========================================
        # EMPTY AUTOMATIC ROW
        # =========================================

        if (
            not product
            and not description
        ):

            return cleaned_data


        # =========================================
        # PRODUCT AND DESCRIPTION
        # CANNOT BOTH BE USED
        # =========================================

        if (
            product
            and description
        ):

            raise forms.ValidationError(
                (
                    "Select a product or enter "
                    "a custom item description. "
                    "You cannot use both."
                )
            )


        # =========================================
        # QUANTITY REQUIRED FOR ACTIVE ROW
        # =========================================

        if quantity is None:

            self.add_error(
                "quantity",
                "Quantity is required.",
            )


        elif quantity <= 0:

            self.add_error(
                "quantity",
                (
                    "Quantity must be greater "
                    "than zero."
                ),
            )


        # =========================================
        # UNIT PRICE REQUIRED
        # =========================================

        if unit_price is None:

            self.add_error(
                "unit_price",
                "Unit price is required.",
            )


        elif unit_price < 0:

            self.add_error(
                "unit_price",
                (
                    "Unit price cannot be "
                    "negative."
                ),
            )


        # =========================================
        # PRODUCT ITEM
        # =========================================

        if product:

            # -------------------------------------
            # PRODUCT DETERMINES TANGIBLE STATE
            # -------------------------------------

            cleaned_data[
                "is_tangible"
            ] = product.is_tangible


            # -------------------------------------
            # ENSURE DESCRIPTION IS EMPTY
            # -------------------------------------

            cleaned_data[
                "description"
            ] = None


        # =========================================
        # CUSTOM ITEM
        # =========================================

        else:

            # -------------------------------------
            # KEEP USER SELECTED TANGIBLE STATE
            # -------------------------------------

            cleaned_data[
                "description"
            ] = description
        # =========================================
        # VALIDATE DELIVERED QUANTITY
        # =========================================

        if (
            self.instance
            and self.instance.pk
            and self.instance.is_tangible
        ):

            delivered_quantity = (
                self.instance.delivered_quantity
            )


            quantity = cleaned_data.get(
                "quantity"
            )


            if (
                quantity is not None
                and quantity < delivered_quantity
            ):

                self.add_error(
                    "quantity",
                    (
                        "Quantity cannot be less than "
                        f"the already delivered quantity "
                        f"of {delivered_quantity}."
                    ),
                )

        return cleaned_data


# =========================================
# QUOTATION ITEM FORMSET
# =========================================


QuotationItemFormSet = (
    inlineformset_factory(
        Quotation,
        QuotationItem,
        form=QuotationItemForm,
        extra=1,
        can_delete=True,
    )
)