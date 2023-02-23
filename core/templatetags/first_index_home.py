from django import template

register = template.Library()

@register.simple_tag(name='get_first_index_home')
def get_first_index_home(stocks, all_stock):
    stocks_list = []
    for stock_item in stocks:
        stocks_list.append(stock_item)

    all_stocks_list = []
    for all_stock_item in all_stock:
        all_stocks_list.append(all_stock_item)

    return all_stocks_list.index(stocks_list[0]) + 1
