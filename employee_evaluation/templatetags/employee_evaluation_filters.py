import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def divide(value, arg):

    try:
        return float(value) / float(arg)

    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
@stringfilter
def remove_specials(string: str):
    return re.sub(r'\s|\W', '', string)
