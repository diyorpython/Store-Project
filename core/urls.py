from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path("verify/", VerifyAccountView.as_view(), name="verify"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password/reset/', views.PasswordResetView.as_view(template_name="auth/password_reset.html"),name="password_reset"),
    path('invoice/', Invoices.as_view(), name='invoice'),
    path('delete/<int:pk>/', DeleteInvoice.as_view(), name='delete'),
    path('delete/confirm/<int:pk>/', ConfirmDeleteInvoice.as_view(), name='delete_confirm'),
    path('invoice/', Invoices.as_view(), name='invoice'),
    path('delete/<int:pk>/', DeleteInvoice.as_view(), name='delete'),
    path('delete/confirm/<int:pk>/', ConfirmDeleteInvoice.as_view(), name='delete_confirm'),
    path('product/',Productlist.as_view(), name='product_list'),
    path('edit_product/<int:pk>/',EditProduct.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/',DeleteProduct.as_view(), name='delete_product'),
    path('delete_confirm/<int:pk>/',ConfirmDeleteProduct.as_view(), name='delete_confirm_product'),
    path('add_product/',AddProduct.as_view(), name='add_product'),
]