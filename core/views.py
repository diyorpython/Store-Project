from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .forms import NewUserForm, ProductForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from config import settings
from .models import Customuser, Invoice, InvoiceItem, Product
from random import randint
from django.views import View
from django_q.tasks import async_task
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class EditProduct(View):
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


class Productlist(View):
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
        return render(request, "core/list_product.html", {"product": products})

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


class DeleteProduct(View):
    template_name = "core/delete_product.html"

    def get(self, request, pk, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'pk': pk})


class ConfirmDeleteProduct(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_list')


class AddProduct(View):
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

class Invoices(View):
    template_name = "invoice/invoice.html"

    def get(self, request, *args, **kwargs):
        invoice = Invoice.objects.all()
        invoiceitem = InvoiceItem.objects.all()
        return render(request=request, template_name=self.template_name,
                      context={'invoice': invoice, 'invoiceitems': invoiceitem})


class DeleteInvoice(View):
    template_name = "invoice/delete_invoice.html"

    def get(self, request, pk, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'pk': pk})


class ConfirmDeleteInvoice(View):
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
                messages.info(request=request, message=f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request=request, message="Invalid username or password")
                return render(request=request, template_name="auth/login.html", context={"form": form})
        else:
            messages.error(request=request, message="Invalid username or password")
            return render(request=request, template_name="auth/login.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request=request)
        messages.info(request=request, message="You are succesfully logout")
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
                        async_task("core.tasks.send_email_reset_password_task", get_current_site(request).domain, "auth/password_reset_text.txt", "Password Reset Requested", user.email, urlsafe_base64_encode(force_bytes(user.pk)), default_token_generator.make_token(user))
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