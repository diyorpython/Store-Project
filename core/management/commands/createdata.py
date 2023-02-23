import json
from pathlib import Path
from django.core.management.base import BaseCommand
from random import randint
from django.utils.text import slugify
from core.models import (
    Category,
    Product,
    Stock,
    Invoice,
    InvoiceItem
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'categories.json') as category_json:
    categories = json.load(category_json)

with open(BASE_DIR / 'products.json') as product_json:
    products = json.load(product_json)

with open(BASE_DIR / 'stock.json') as stock_json:
    stock = json.load(stock_json)

with open(BASE_DIR / 'invoice.json') as invoice_json:
    invoices = json.load(invoice_json)

with open(BASE_DIR / 'invoiceitem.json') as invoiceitem_json:
    invoiceitems = json.load(invoiceitem_json)

class Command(BaseCommand):
    help = 'Create random data and add to database'

    def handle(self, *args, **options):
        categories_len = len(categories)
        for category in categories:
            try:
                Category.objects.create(**category)
            except Exception:
                categories_len -= 1
        if categories_len == 0:
            self.stdout.write('Everything up-to-date')
        else:
            plural = 'ies' if categories_len > 1 else 'y'
            self.stdout.write(f'{categories_len} categor{plural} data created successfully!!!')

# --------------------------------------------------------------------------------------------------------------------------------------- #

        products_len = len(products)
        def get_random_category():
            categories_list = [exist_category for exist_category in Category.objects.all()]
            random_id = randint(0, len(categories_list)-1)

            return categories_list[random_id]

        for product in products:
            try:
                product['category'] = get_random_category()
                product['code'] = slugify(product['name'])
                Product.objects.create(**product)
            except Exception:
                products_len -= 1
        if products_len == 0:
            self.stdout.write('Everything up-to-date')
        else:
            plural = 's' if products_len > 1 else ''
            self.stdout.write(f'{products_len} product{plural} data created successfully!!!')

# ------------------------------------------------------------------------------------------------------------------------------------- #

        stocks_len = len(stock)
        def get_random_product():
            products_list = [exist_product for exist_product in Product.objects.all()]
            random_id = randint(0, len(products_list)-1)
            return products_list[random_id]

        for stock_item in stock:
            try:
                stock_item['product'] = get_random_product()
                Stock.objects.create(**stock_item)
            except Exception:
                stocks_len -= 1
        if stocks_len == 0:
            self.stdout.write('Everything up-to-date')
        else:
            plural = 's' if stocks_len > 1 else ''
            self.stdout.write(f'{stocks_len} stock{plural} data created successfully!!!')

# ---------------------------------------------------------------------------------------------------------------------------------- #

        invoices_len = len(invoices)
        for invoice in invoices:
            try:
                Invoice.objects.create(**invoice)
            except Exception:
                invoices_len -= 1
        if invoices_len == 0:
            self.stdout.write('Everything up-to-date')
        else:
            plural = 's' if invoices_len > 1 else ''
            self.stdout.write(f'{invoices_len} invoice{plural} data created successfully!!!')

# ---------------------------------------------------------------------------------------------------------------------------------- #

        invoiceitems_len = len(invoiceitems)
        def get_random_product():
            products_list = [exist_product for exist_product in Product.objects.all()]
            random_id = randint(0, len(products_list)-1)
            return products_list[random_id]

        def get_random_invoice():
            invoices_list = [exist_invoice for exist_invoice in Invoice.objects.all()]
            random_id = randint(0, len(invoices_list)-1)
            return invoices_list[random_id]

        def get_random_stock():
            stocks_list = [exist_stock for exist_stock in Stock.objects.all()]
            random_id = randint(0, len(stocks_list)-1)
            return stocks_list[random_id]

        for invoiceitem in invoiceitems:
            try:
                invoiceitem['product'] = get_random_product()
                invoiceitem['invoice'] = get_random_invoice()
                invoiceitem['stock'] = get_random_stock()
                InvoiceItem.objects.create(**invoiceitem)
            except Exception:
                invoiceitems_len -= 1
        if invoiceitems_len == 0:
            self.stdout.write('Everything up-to-date')
        else:
            plural = 's' if invoiceitems_len > 1 else ''
            self.stdout.write(f'{invoiceitems_len} invoiceitem{plural} data created successfully!!!')
