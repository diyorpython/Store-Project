from django.urls import path
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path("verify/", VerifyAccountView.as_view(), name="verify"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password/reset/', views.PasswordResetView.as_view(template_name="auth/password_reset.html"), name="password_reset"),
    path('invoice/', Invoices.as_view(), name='invoice'),
    path('delete/<int:pk>/', DeleteInvoice.as_view(), name='delete'),
    path('delete/confirm/<int:pk>/', ConfirmDeleteInvoice.as_view(), name='delete_confirm'),
    path('product/', Productlist.as_view(), name='product_list'),
    path('edit_product/<int:pk>/', EditProduct.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
    path('delete_confirm/<int:pk>/', ConfirmDeleteProduct.as_view(), name='delete_confirm_product'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('detail/<int:pk>', DetailProduct.as_view(), name='detail'),
    path('categories/', CategoryList.as_view(), name='categories_list'),
    path('edit_categories/<int:pk>/', EditCategory.as_view(), name='edit_categories'),
    path('delete_categories/<int:pk>/', DeleteCategory.as_view(), name='delete_categories'),
    path('delete_confirm_category/<int:pk>/',ConfirmDeleteCategory.as_view(), name='delete_confirm_categories'),
    path('add_categories/', AddCategory.as_view(), name='add_categories'),
    path('inventory/', InventoryView.as_view(), name='inventory_home'),
    path('inventory/<int:pk>/', InventoryByIdView.as_view(), name='inventory_action'),
    path('history/delete/<int:pk>/', DeleteHistoryView.as_view(), name='delete_history'),
    path('transaction/add/', AddTransactionView.as_view(), name='transaction_add'),
    path('history/edit/<int:pk>/', EditHistoryView.as_view(), name='edit_history'),
    path("user/", UserProfileView.as_view(), name="user_profile"),
    path("edit_user/", EditUserProfile.as_view(), name="edit_user"),
]