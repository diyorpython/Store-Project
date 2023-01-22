from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .managers import (
    ActiveCategoryCustomManager,
    ActiveProductCustomManager,
    CustemUserManager,
)
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    PermissionsMixin,
)


def min_value_validator(value):
    if value < 0:
        raise ValidationError(
            '%(value)s must be greater than or equal to 0',
            params={'value': value},
        )


class BaseModel(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'Base Model'


class Category(BaseModel):
    STATUSES = (
        ('0', 'Stack-out'),
        ('1', 'Stack-in')
    )

    name = models.CharField(
        verbose_name='Category name',
        max_length=255,
        unique=True
    )
    description = models.TextField(
        verbose_name='Category description'
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        choices=STATUSES,
        default=STATUSES[0][0]
    )

    objects = models.Manager()
    objects_in_stock = ActiveCategoryCustomManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseModel):
    STATUSES = (
        ('0', 'InActive'),
        ('1', 'Active')
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='Category'
    )
    name = models.CharField(
        verbose_name='Product name',
        max_length=255
    )
    code = models.SlugField(null=True, blank=True)
    description = models.TextField(
        verbose_name='Product description'
    )
    price = models.DecimalField(
        verbose_name='Product price',
        max_digits=10,
        decimal_places=2,
        validators=[min_value_validator]
    )
    status = models.CharField(
        verbose_name='Product status',
        max_length=10,
        choices=STATUSES,
        default=STATUSES[0][0]
    )

    objects = models.Manager()
    active_objects = ActiveProductCustomManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'Products'

    def save(self, *args, **kwargs):
        id = self.pk
        stock = Stock.objects.filter(product__id=id)
        if stock.exists():
            if stock[0].type == '1':
                self.status = '1'
            else:
                self.status = '0'
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Stock(BaseModel):
    TYPES = (
        ('0', 'Stock-out'),
        ('1', 'Stock-in')
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Product quantity',
        default=0,
        validators=[min_value_validator]
    )
    type = models.CharField(
        max_length=10,
        choices=TYPES,
        default=TYPES[0][0]
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
        db_table = 'Stock'

    def save(self, *args, **kwargs):
        product = Product.objects.filter(id=self.product.id)
        if product.exists():
            if self.quantity > 0:
                self.type = '1'
                Product.objects.update(id=product[0].id, status='1')
            else:
                self.type = '0'
                Product.objects.update(id=product[0].id, status='0')
        super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name


class Invoice(BaseModel):
    transaction = models.CharField(
        max_length=255
    )
    customer = models.CharField(
        max_length=255
    )
    total = models.DecimalField(
        verbose_name='Total price',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        db_table = 'Invoices'

    def __str__(self):
        return self.transaction


class InvoiceItem(BaseModel):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='Product'
    )
    invoice = models.ForeignKey(
        to=Invoice,
        on_delete=models.CASCADE,
        related_name='Invoice'
    )
    stock = models.ForeignKey(
        to=Stock,
        on_delete=models.CASCADE,
        related_name='Stock'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[min_value_validator]
    )
    quantity = models.PositiveBigIntegerField(
        default=0,
        validators=[min_value_validator]
    )

    class Meta:
        verbose_name = 'InvoiceItem'
        verbose_name_plural = 'InvoiceItmes'
        db_table = 'InvoiceItems'

    def save(self, *args, **kwargs):
        if self.stock.quantity < self.quantity:
            raise ValueError('Oops we haven\'t got enaugh product!')
        else:
            stock_quantity = self.stock.quantity - self.quantity
            Stock.objects.update(id=self.stock.id, quantity=stock_quantity)
        return super(InvoiceItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name


class Customuser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        null=True,
    )
    full_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True)
    addres = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_code = models.PositiveIntegerField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustemUserManager()

    def __str__(self):
        return self.email
