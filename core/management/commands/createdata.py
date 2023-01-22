import json
from pathlib import Path
from django.core.management.base import BaseCommand
from random import randint
from django.utils.text import slugify
from core.models import (
    Category,
    Product,
    Stock
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / 'categories.json') as category_json:
    categories = json.load(category_json)

with open(BASE_DIR / 'products.json') as product_json:
    products = json.load(product_json)

with open(BASE_DIR / 'stock.json') as stock_json:
    stock = json.load(stock_json)


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
            plural = 'ies' if categories_len > 0 else 'y'
            self.stdout.write(f'{categories_len} categor{plural} data created successfully!!!')

        products_len = len(products)
        def get_random_category():
            categories_list = [exist_category for exist_category in Category.objects.all()]
            random_id = randint(1, len(categories_list))
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
            plural = 's' if products_len > 0 else ''
            self.stdout.write(f'{products_len} product{plural} data created successfully!!!')