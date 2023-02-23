from django import template

register = template.Library()

@register.simple_tag(name='sum_of_value')
def get_sum_of_value(obj):
    result = 0
    for item in obj:
        result += item.quantity
    
    return result
