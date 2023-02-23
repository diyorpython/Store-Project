from django.shortcuts import render, get_object_or_404
from .serializers import InvoiceSerializer, InvoiceItemSerializer, ProductSerializer, CategorySerializer, InventorySerializer, UserSerializer
from core.models import Invoice, InvoiceItem, Product, Category, Stock, History
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

# Invoice
class InvoicesView(APIView, PageNumberPagination):
    serializer_class = InvoiceSerializer
    page_size = 3
    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        result = self.paginate_queryset(invoices, request, view=self)
        serializer = self.serializer_class(instance=result, many=True)
        return self.get_paginated_response(serializer.data)
        # return Response(data=serializer.data)

    
class InvoiceView(APIView):
    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        serializer = InvoiceSerializer(instance=invoice)
        return Response(data=serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        return Response({"Deleted": "Invoice was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class InvoicesItemView(APIView):
    def get(self, request, *args, **kwargs):
        invoices = InvoiceItem.objects.all()
        serializer = InvoiceItemSerializer(instance=invoices, many=True)
        return Response(data=serializer.data)


class InvoiceItemView(APIView):
    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(InvoiceItem, pk=pk)
        serializer = InvoiceItemSerializer(instance=invoice)
        return Response(data=serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(InvoiceItem, pk=pk)
        invoice.delete()
        return Response({"Deleted": "Invoice was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class ProductListCreateAPIView(APIView,PageNumberPagination):
    page_size = 3
    serializer_class = ProductSerializer
    def get(self,request,*args,**kwargs):
        product = Product.objects.all()
        results = self.paginate_queryset(product, request, view=self)
        serializer =self.serializer_class(results,many=True)
        return self.get_paginated_response(serializer.data)
        # return Response(data=serializer.data)

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)


class ProductRetirieveUpdateDeleteAPIView(APIView):
    serializer_class = ProductSerializer
    def get(self,request,pk):
        ganre = get_object_or_404(Product, id=pk)
        serializer = self.serializer_class(ganre)
        return Response(data=serializer.data)
    def put(self, request,pk):
        data= request.data
        ganre = get_object_or_404(Product, id=pk)
        serializer =self.serializer_class(instance=ganre,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
        

    def patch(self, request,pk):
        data= request.data
        ganre = get_object_or_404(Product, id=pk)
        serializer =self.serializer_class(instance=ganre,data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


    def delete(self, request,pk):
        ganre = get_object_or_404(Product, id=pk)
        ganre.delete()
        return Response(data={"deleted":"product"},status=status.HTTP_204_NO_CONTENT)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data,
                                    context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CategoryListCreateAPIView(APIView):
    serializer_class = CategorySerializer
    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class CategoryRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = CategorySerializer
    def get(self, request, id):
        categories = get_object_or_404(Category, id=id)
        serializer = self.serializer_class(categories)
        return Response(data=serializer.data)
    
    def put(self, request, id):
        data = request.data
        categories = get_object_or_404(Category, id=id)
        serializer = self.serializer_class(instance=categories, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, id):
        data = request.data
        categories = get_object_or_404(Category, id=id)
        serializer = self.serializer_class(instance=categories, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, id):
        categories = get_object_or_404(Category, id=id)
        categories.delete()
        return Response(data={"deleted": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        

# inventory
class InventoryApiView(APIView, PageNumberPagination):
    serializer_class = InventorySerializer
    page_size = 5
    
    def get(self, request, *args, **kwargs):
        stock = Stock.objects.all()
        result = self.paginate_queryset(stock, request, view=self)
        serializer = self.serializer_class(result, many=True)
        return Response(data=serializer.data, status=200)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)
    
    
class InventoryByIdApiView(APIView):
    serializer_class = InventorySerializer
    
    def get(self, request, pk, *args, **kwargs):
        stock = Stock.objects.get(pk=pk)
        history = History.objects.filter(stock=stock)
        serializer = self.serializer_class(history)
        return Response(data=serializer.data, status=200)
    
    def put(self, request, pk, *args, **kwargs):
        stock = Stock.objects.get(pk=pk)
        history = History.objects.filter(stock=stock)
        data = request.data
        serializer = self.serializer_class(instance=history, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)
    
    def patch(self, request, pk, *args, **kwargs):
        stock = Stock.objects.get(pk=pk)
        history = History.objects.filter(stock=stock)
        data = request.data
        serializer = self.serializer_class(instance=history, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)
    
    def delete(self, request, pk, *args, **kwargs):
        stock = Stock.objects.get(pk=pk)
        history = History.objects.filter(stock=stock)
        history_id = history.pk
        history.delete()
        return Response(data={f'{history_id} - history deleted successfully!'}, status=204)
