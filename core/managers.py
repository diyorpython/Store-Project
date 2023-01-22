from django.db import models
from django.db.models import Q
from . import models as model
from django.contrib.auth.base_user import BaseUserManager


class ActiveCategoryCustomQuerySet(models.QuerySet):
    def all(self):
        all_active_categories = self.filter(status='1')
        return all_active_categories

    def info(self, name):
        try:
            category = self.get(name=name)
        except Exception:
            raise ValueError('Category doesn\'t exist')
        else:
            category_date_created = category.date_created
            category_date_updated = category.date_updated
            category_date_created = category.date_created
            category_date_updated = category.date_updated
            category_name = name
            category_description = category.description
            category_status = 'Stock-in' if category.status == '1' else 'Stock-out'
            category_verbose_name = self.model._meta.verbose_name
            category_verbose_name_plural = self.model._meta.verbose_name_plural
            category_DB_table_name = self.model._meta.db_table
            return f'----- {category} -----\n' \
                f'Name - {category_name}\n' \
                f'Description - {category_description}\n' \
                f'Status - {category_status}\n' \
                f'Verbose name - {category_verbose_name}\n' \
                f'Verbose name plural - {category_verbose_name_plural}\n' \
                f'DB table name - {category_DB_table_name}\n' \
                f'Created - {category_date_created}\n' \
                f'Updated - {category_date_updated}'

    def count_of_products(self):
        try:
            categories = self.all()
        except Exception:
            raise ValueError('Somthing went wrong')
        else:
            result = ''
            for category in categories:
                products = model.Product.objects.filter(category__id=category.id)
                result += f'\n----- {category} -----\n'
                iter_count = 0
                for product in products:
                    iter_count += 1
                    result += f'{iter_count} - {product}'
            if result != '':
                return result
            else:
                return 'empty'

    def get_product(self, name):
        try:
            category = self.get(name=name)
        except Exception:
            return 'Category not found'
        else:
            products = model.Product.objects.filter(category__id=category.id)
            if products:
                result = f'\n----- {category} -----\n'
                iter_count = 0
                for product in products:
                    iter_count += 1
                    product_status = 'Active' if product.status == '1' else 'Inactive'
                    result += f'{iter_count} - {product} - {product_status}'
                return result
            else:
                return 'Haven\'t got any product in this category'

    def search(self, query=None):
        bad_request = ('', None, [], {}, ())
        if query not in bad_request:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            result = self.filter(lookups, status='1')
            if result:
                return result
            else:
                return 'Nothing found'
        return self.none()


class ActiveCategoryCustomManager(models.Manager):
    def get_queryset(self):
        return ActiveCategoryCustomQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def info(self, name):
        return self.get_queryset().info(name=name)

    def count_of_products(self):
        return self.get_queryset().count_of_products()

    def get_product(self, name):
        return self.get_queryset().get_product(name=name)

    def search(self, query):
        return self.get_queryset().search(query=query)


class ActiveProductCustomQuerySet(models.QuerySet):
    def all(self):
        all_active_categories = self.filter(status='1')
        return all_active_categories

    def info(self, name):
        try:
            product = self.get(name=name)
        except Exception:
            raise ValueError('Category doesn\'t exist')
        else:
            product_date_created = product.date_created
            product_date_updated = product.date_updated
            product_date_created = product.date_created
            product_date_updated = product.date_updated
            product_category = product.category
            product_name = name
            product_code = product.code
            product_description = product.description
            product_price = product.price
            product_status = 'Stock-in' if product.status == '1' else 'Stock-out'
            product_verbose_name = self.model._meta.verbose_name
            product_verbose_name_plural = self.model._meta.verbose_name_plural
            product_DB_table_name = self.model._meta.db_table
            return f'----- {product} -----\n' \
                f'Category - {product_category}\n' \
                f'Code - {product_code}' \
                f'Name - {product_name}\n' \
                f'Description - {product_description}\n' \
                f'Price - {product_price}\n' \
                f'Status - {product_status}\n' \
                f'Verbose name - {product_verbose_name}\n' \
                f'Verbose name plural - {product_verbose_name_plural}\n' \
                f'DB table name - {product_DB_table_name}\n' \
                f'Created date - {product_date_created}\n' \
                f'Updated date - {product_date_updated}'

    def count_in_stock(self):
        try:
            products = self.all()
        except Exception:
            raise ValueError('Somthing went wrong')
        else:
            result = ''
            for product in products:
                stock = model.Stock.objects.filter(product__id=product.id)
                result += f'{product} -- {len(stock)}'
            if result != '':
                return result
            else:
                return 'empty'

    def search(self, query=None):
        bad_request = ('', None, [], {}, ())
        if query not in bad_request:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            result = self.filter(lookups)
            if result:
                return result
            else:
                return 'Nothing found'
        return self.none()


class ActiveProductCustomManager(models.Manager):
    def get_queryset(self):
        return ActiveProductCustomQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def info(self, name):
        return self.get_queryset().info(name=name)

    def count_in_stock(self):
        return self.get_queryset().count_in_stock()

    def search(self, query):
        return self.get_queryset().search(query=query)


class CustemUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Emailni kiriting")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Super user must have is_acrive=True")
        return self.create_user(email, password, **extra_fields)
