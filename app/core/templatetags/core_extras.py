from django import template
from django_cardano.settings import django_cardano_settings

register = template.Library()

lovelace_unit = django_cardano_settings.LOVELACE_UNIT

@register.filter
def toada(value):
    return value / 1000000


@register.filter
def token_list(value: dict) -> str:
    icon_class = 'fas fa-coins cursor-pointer'
    list_items = []
    tokens = dict(value)

    ada_value = toada(tokens[lovelace_unit])
    formatted_ada_value = '{:.6f}'.format(ada_value)
    list_items.append(f'<p>₳ {formatted_ada_value}</p>')
    del tokens[lovelace_unit]

    for asset_id, quantity in tokens.items():
        list_items.append(f'<p><i class="{icon_class}" title="{asset_id}"></i> {quantity}</p>')

    return ''.join(list_items)
