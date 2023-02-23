from rest_framework import serializers
from core.models import (
    Invoice,
    InvoiceItem,
    Product,
    Category,
    Customuser,
    History,
    Stock
)

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'date_created', 'date_updated', 'transaction', 'customer', 'total')

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('id', 'date_created', 'date_updated', 'product', 'invoice', 'stock', 'price', 'quantity')

        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

        read_only_fields = ('date_created', 'date_updated')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ('id', "username", "full_name", "email", "password1", "password2")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"  
        read_only_fields = ('date_created', 'date_updated')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"  
        read_only_fields = ('date_created', 'date_updated')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"  
        read_only_fields = ('date_created', 'date_updated')