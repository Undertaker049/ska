from django import template

register = template.Library()


@register.filter
def split(value, arg):
    return value.split(arg)


@register.filter
def map(value, arg):
    return [getattr(item, arg)() if callable(getattr(item, arg)) else getattr(item, arg) for item in value]