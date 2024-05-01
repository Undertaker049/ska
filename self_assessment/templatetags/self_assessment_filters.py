from django import template

register = template.Library()


@register.filter
def replace_dj(value: str, args: str):
    args = args.split('|')
    return value.replace(args[0], args[1])


@register.filter
def get_level_val(value: str):
    return value.split(" ")[0]
