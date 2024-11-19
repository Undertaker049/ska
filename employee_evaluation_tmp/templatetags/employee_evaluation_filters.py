from django import template

register = template.Library()


@register.filter
def div(value, arg):

    try:
        return float(value) / float(arg)

    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def mul(value, arg):

    try:
        return float(value) * float(arg)

    except ValueError:
        return 0


@register.filter
def get(dictionary, key):
    return dictionary.get(key)


@register.filter
def remove_specials(value):
    return "".join(e for e in value if e.isalnum())