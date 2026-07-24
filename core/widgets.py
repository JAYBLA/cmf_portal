from decimal import Decimal, InvalidOperation

from django.forms import NumberInput


class IntegerDisplay(NumberInput):   

    def format_value(self, value):
        if value in (None, ""):
            return ""

        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return super().format_value(value)

        if value == value.to_integral_value():
            return str(int(value))

        return str(value.normalize())