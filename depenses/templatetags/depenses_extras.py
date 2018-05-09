from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def subtractify(context, obj):
    newval = obj.loan_amount - obj.service_charge
    return newval