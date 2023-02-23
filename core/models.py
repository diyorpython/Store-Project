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

    product = models.OneToOneField(
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
        ordering = ['-date_created']

    def save(self, commit=True, *args, **kwargs):
        product = Product.objects.filter(id=self.product.pk)
        if product.exists():
            if not self.pk:
                if self.quantity > 0:
                    self.type = '1'
                    product = Product.objects.get(id=product.first().pk)
                    product.status = '1'
                    product.save()
                else:
                    self.type = '0'
                    product = Product.objects.get(id=product.first().pk)
                    product.status = '0'
                    product.save()
                super(Stock, self).save(*args, **kwargs)
                stock = Stock.objects.get(id=self.pk)
                if commit:
                    History.objects.create(stock=stock, quantity=self.quantity, type=self.type)
            else:
                stock = Stock.objects.get(id=self.pk)
                if self.quantity > stock.quantity:
                    if commit:
                        History.objects.create(stock=stock, quantity=self.quantity-stock.quantity, type='1')
                elif self.quantity == stock.quantity:
                    pass
                else:
                    if commit:
                        History.objects.create(stock=stock, quantity=stock.quantity-self.quantity, type='0')
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
            stock = Stock.objects.get(id=self.stock.pk)
            stock.quantity = stock_quantity
            stock.save()
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


class History(BaseModel):
    STOCK_IN = '1'
    STOCK_OUT = '0'

    TYPES = (
        (STOCK_IN, 'stock-in'),
        (STOCK_OUT, 'stock-out')
    )

    stock = models.ForeignKey(
        to=Stock,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='quantity'
    )
    type = models.CharField(
        verbose_name='type',
        max_length=12,
        choices=TYPES
    )

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Histories'
        db_table = 'History'
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.pk:
            history = History.objects.get(id=self.pk)
            if history.quantity < self.quantity:
                self.stock.quantity += self.quantity - history.quantity
                self.stock.save(commit=False)
            else:
                self.stock.quantity -= history.quantity - self.quantity
                self.stock.save(commit=False)
        elif self.quantity == 0:
            pass
        super(History, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.type == self.STOCK_IN:
            if self.stock.quantity - self.quantity >= 0:
                self.stock.quantity -= self.quantity
                self.stock.save(commit=False)
            else:
                raise ValueError('Haven\'t got enaugh product!')
        else:
            if self.stock.quantity + self.quantity >= 0:
                self.stock.quantity += self.quantity
                self.stock.save(commit=False)
            else:
                raise ValueError('Haven\'t got enaugh product!')
        super(History, self).delete(*args, **kwargs)

    def __str__(self):
        return self.stock.product.name


class Sales(BaseModel):
    user = models.CharField(
        verbose_name='User',
        max_length=255
    )
    stock = models.ForeignKey(
        to=Stock,
        on_delete=models.CASCADE,
        related_name='Product'
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name='Quantity'
    )

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        db_table = 'Sales'
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            if self.stock.quantity - self.quantity >= 0:
                self.stock.quantity -= self.quantity
                self.stock.save()
            else:
                raise ValueError('Haven\'t got enaugh product!')
            super(Sales, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.stock.product.name}'

class UserProfile(models.Model):
    user          = models.OneToOneField(to=Customuser, on_delete=models.CASCADE)
    bio           = models.TextField()
    image         = models.ImageField(null=True, blank=True, upload_to="profiles")
    phone_number  = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return f"{self.user.username}"