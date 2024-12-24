from django import template

register = template.Library()


@register.filter
def replace_dj(value, arg):
    """Заменяет символы в строке"""
    old, new = arg.split('|')
    return value.replace(old, new)

@register.filter
def get_item(dictionary, key):
    """Получает значение из словаря по ключу"""
    return dictionary.get(str(key), [])
