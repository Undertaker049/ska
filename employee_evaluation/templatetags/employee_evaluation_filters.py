import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def remove_specials(string: str):
    return re.sub(r'\s|\W', '', string)
