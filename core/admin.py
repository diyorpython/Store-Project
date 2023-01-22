from django.contrib import admin
from .models import (
    Category,
    Product,
    Stock,
    Invoice,
    InvoiceItem,
    Customuser
)


uneditable_fields = ('id', 'date_created', 'date_updated')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'status'
    )
    fields = [field.name for field in Category._meta.fields if field.name not in uneditable_fields]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'price',
        'status',
    )
    fields = [field.name for field in Product._meta.fields if field.name not in uneditable_fields]
    prepopulated_fields = {'code': ('name',)}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'type'
    )
    fields = [field.name for field in Stock._meta.fields if field.name not in uneditable_fields]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'transaction',
        'customer',
        'total'
    )
    fields = [field.name for field in Invoice._meta.fields if field.name not in uneditable_fields]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'invoice',
        'price',
        'quantity'
    )
    fields = [field.name for field in InvoiceItem._meta.fields if field.name not in uneditable_fields]

@admin.register(Customuser)
class CustomuserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'full_name',
        'email',
        'addres',
        'is_staff',
        'is_active',
        'date_joined'
    )
    fields = [field.name for field in Customuser._meta.fields if field.name not in uneditable_fields]