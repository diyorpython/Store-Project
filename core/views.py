from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .forms import NewUserForm, ProductForm, CategoryForm, HistoryForm, TransactionForm, UserForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import BadHeaderError
from .models import Customuser, Invoice, InvoiceItem, Product, Category
from random import randint
from django.views import View
from django_q.tasks import async_task
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        # Show stats => products, categories, transactions (sales)
        return render(request, "core/index.html")


class EditProduct(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, "core/edit_product.html", {'form': form, 'pk': pk})

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, "core/edit_product.html", {"form": form, 'pk': pk})


class Productlist(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all().order_by("-date_created")
        paginator = Paginator(products, 5)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request,"core/list_product.html",{"product":products})
    def post(self, request):
        products = Product.objects.all().order_by("date_created")
        paginator = Paginator(products, 5)

        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, "core/list_product.html", {"product": products})


class DeleteProduct(LoginRequiredMixin, View):
    template_name = "core/delete_product.html"

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        return render(request=request, template_name=self.template_name, context={'pk': pk, 'product_info': product})
    

class DetailProduct(LoginRequiredMixin, View):
    template_name = "core/detail.html"
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        return render(request=request, template_name=self.template_name, context={'pk': pk, 'detail': product})


class ConfirmDeleteProduct(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_list')


class AddProduct(LoginRequiredMixin, View):
    template_name = "core/add_product.html"

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
        else:
            return render(request, self.template_name, {"form": form})

# -- Invoice View --

class Invoices(LoginRequiredMixin, View):
    template_name = "invoice/invoice.html"

    def get(self, request, *args, **kwargs):
        invoice = Invoice.objects.all()
        invoiceitem = InvoiceItem.objects.all()
        paginator = Paginator(invoice, 5)

        page = request.GET.get('page')
        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            invoices = paginator.page(1)
        except EmptyPage:
            invoices = paginator.page(paginator.num_pages)
        return render(request=request, template_name=self.template_name, context={'invoice': invoices, 'invoiceitems': invoiceitem})

class DeleteInvoice(LoginRequiredMixin, View):
    template_name = "invoice/delete_invoice.html"

    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        return render(request=request, template_name=self.template_name, context={'p_key': pk, 'deleted_invoice': invoice})


class ConfirmDeleteInvoice(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        messages.success(request, "Invoice was successfully deleted")
        return redirect('invoice')


# -- Authentication View --

class RegisterView(View):
    def get(self, request):
        form = NewUserForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            code = randint(100000, 999999)
            user.is_active = False
            user.email_code = code
            user.uid = urlsafe_base64_encode(force_bytes(user.email))
            user.token = default_token_generator.make_token(user)
            user.save()
            try:
                async_task("core.tasks.send_email_task", code, get_current_site(request).domain, "auth/email_verification_text.txt", "Email Verification", user.email)
                return redirect("verify")
            except BadHeaderError:
                return HttpResponse("Invalid header error")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, "auth/register.html", {"form": form})


class LoginUserView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request=request, template_name="auth/login.html", context={"form": form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request=request, user=user)
                messages.success(request=request, message=f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request=request, message="Invalid username or password")
                return render(request=request, template_name="auth/login.html", context={"form": form})
        else:
            messages.error(request=request, message="Invalid username or password")
            return render(request=request, template_name="auth/login.html", context={"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request=request)
        messages.success(request=request, message="You are succesfully logout")
        return redirect("index")


class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request=request, template_name="auth/password_reset.html", context={"form": form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            users = Customuser.objects.filter(Q(email=email))
            if users.exists():
                for user in users:
                    try:
                        async_task("core.tasks.send_email_reset_password_task", get_current_site(request).domain, "auth/password_reset_text.txt", "Password Reset Requested", [user.email], urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user))
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("index")


class VerifyAccountView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "auth/verify_email.html")

    def post(self, request):
        code = request.POST.get("code")
        print(code)
        if code.isdigit():
            user = Customuser.objects.filter(email_code=code)
            print(user)
            if user.exists():
                user = user.last()
                user.is_active = True
                user.save()
                login(request, user)
                return redirect("product_list")
            else:
                messages.error(request, "Invalid verify code")
                return redirect("verify")
        else:
            messages.error(request, "Verify code should be number")
            return redirect("verify")

class CategoryList(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all().order_by("-date_created")
        paginator = Paginator(categories, 5)

        page = request.GET.get('page')
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        return render(request,"core/list_categories.html",{"categories":categories})
    
class EditCategory(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        categories = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=categories)
        return render(request,"core/edit_categories.html",{'form':form, 'pk':pk})

    def post(self, request, pk, *args, **kwargs):
        categories = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=categories)
        if form.is_valid():
             form.save()
             return redirect('categories_list')
        return render(request, "core/edit_categories.html", {"form": form, 'pk':pk})

class DeleteCategory(View):
    template_name = "core/delete_categories.html"
    def get(self, request, pk, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'pk': pk})

class AddCategory(LoginRequiredMixin, View):
    template_name = "core/add_categories.html"
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("categories_list")
        else:
            return render(request, self.template_name, {"form": form})

class ConfirmDeleteCategory(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        categories = get_object_or_404(Category, pk=pk)
        categories.delete()
        return redirect('categories_list')

# Inventory

class InventoryView(View):
    template_name = 'inventory/inventory_home.html'

    def get(self, request, *args, **kwargs):
        stock = Stock.objects.all()
        stock_length = len(stock)
        all_stock = stock
        paginator = Paginator(stock, 5)

        page = request.GET.get('page')
        try:
            stock = paginator.page(page)
        except PageNotAnInteger:
            stock = paginator.page(1)
        except EmptyPage:
            stock = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'stocks': stock,
            'stock_length': stock_length,
            'all_stock': all_stock
        })


class InventoryByIdView(View):
    template_name = 'inventory/inventory_action.html'

    def get(self, request, pk, *args, **kwargs):
        stock = Stock.objects.get(pk=pk)
        try:
            history = History.objects.filter(stock__pk=stock.pk)
        except Exception:
            history = None
        all_histories = history
        history_len = len(history)
        paginator = Paginator(history, 5)

        form = HistoryForm()

        page = request.GET.get('page')
        try:
            history = paginator.page(page)
        except PageNotAnInteger:
            history = paginator.page(1)
        except EmptyPage:
            history = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'stock': stock,
            'histories': history,
            'history_len': history_len,
            'all_histories': all_histories,
            'form': form
        })


class DeleteHistoryView(View):
    def get(self, request, pk, *args, **kwargs):
        history = get_object_or_404(History, pk=pk)
        stock_id = history.stock.pk
        try:
            history.delete()
        except ValueError:
            messages.error(
                request=request,
                message='Haven\'t got enaugh Product!'
            )
            return redirect('inventory_action', stock_id)
        messages.info(
            request=request,
            message='History deleted successfully!'
        )
        return redirect('inventory_action', stock_id)


class EditHistoryView(View):
    template_name = 'inventory/history_edit.html'

    def get(self, request, pk, *args, **kwargs):
        history = get_object_or_404(History, pk=pk)
        form = HistoryForm(instance=history)
        return render(request, self.template_name, {
            'form': form,
            'pk': pk
        })

    def post(self, request, pk, *args, **kwargs):
        history = get_object_or_404(History, pk=pk)
        stock_id = history.stock.pk
        form = HistoryForm(data=request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(
                request=request,
                message='History edited successfully!'
            )
            return redirect('inventory_action', stock_id)
        else:
            messages.error(
                request=request,
                message='Invalid form filled!'
            )
            return redirect('inventory_action', stock_id)


class AddTransactionView(View):
    template_name = 'inventory/transaction_add.html'

    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(
            request=request,
            message='Transaction added successfully!'
        )
            return redirect('inventory_home')
        else:
            messages.error(
                request=request,
                message='Error while creating Transaction'
            )
            return redirect('transaction_add')

    
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = Customuser.objects.get(id=request.user.id)
        user1 = UserProfile.objects.get(user=request.user)
        return render(request, "core/user_profile.html", {"user": user, "user1": user1})
    
class EditUserProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = Customuser.objects.get(id=request.user.id)
        form = UserForm(instance=user)
        user1 = UserProfile.objects.get(user=request.user)
        form1 = UserProfileForm(instance=user1)
        return render(request, "core/edit_user_profile.html", {"form": form, "form1": form1})

    def post(self, request):
        user = Customuser.objects.get(id=request.user.id)
        user1 = UserProfile.objects.get(user=request.user)
        form = UserForm(data=request.POST, files=request.FILES, instance=user)
        form1 = UserProfileForm(data=request.POST, instance=user1)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()

            return redirect("user_profile")
        
        else:
            messages.error(request, "User not found")
            return redirect("user_profile")