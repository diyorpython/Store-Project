from django import template

register = template.Library()

@register.simple_tag(name='InvoiceFunction')
def InvoiceFunction(invoice, invoiceitems):
    result = 0
    for invoiceitem in invoiceitems:
        if invoiceitem.invoice == invoice:
            result += invoiceitem.quantity
    return result