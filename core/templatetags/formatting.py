from decimal import Decimal

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def money(value, decimals=0):
    if value in (None, ""):
        return ""

    value = Decimal(value)

    if int(decimals) == 0:
        return intcomma(f"{value:.0f}")

    return intcomma(f"{value:.{int(decimals)}f}")