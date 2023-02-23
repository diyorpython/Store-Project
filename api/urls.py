from django.urls import path
from .views import *

urlpatterns = [
    path('invoices/', InvoicesView.as_view()),
    path('invoice/<int:pk>/', InvoiceView().as_view()),
    path('invoiceitem/<int:pk>/', InvoiceItemView.as_view()),
    path('invoiceitems/', InvoicesItemView.as_view()),
    path('product/',ProductListCreateAPIView.as_view()),
    path('product/<int:pk>/',ProductRetirieveUpdateDeleteAPIView.as_view()),
    path('category/', CategoryListCreateAPIView.as_view()),
    path('category/<int:id>/',CategoryRetrieveUpdateDeleteAPIView.as_view()),
    path('inventory/', InventoryApiView.as_view()),
    path('inventory/<int:pk>/', InventoryByIdApiView.as_view())
]
