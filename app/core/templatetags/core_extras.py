from django import template

register = template.Library()


@register.filter
def toada(value):
    return value / 1000000
