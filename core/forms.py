from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customuser, Product, Category, History, Sales, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ("category","name", "code","description","price","status")

class NewUserForm(UserCreationForm):
    email = forms.CharField(required=True)

    class Meta:
        model = Customuser
        fields = ("username", "full_name" ,"email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ("name", "description", "status")


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = (
            'stock',
            'quantity'
        )


class TransactionForm(forms.ModelForm):
    class Meta:
        model  = Sales
        fields = (
            'user',
            'stock',
            'quantity'
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = Customuser
        fields = ("username", "email", "full_name", "addres")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("bio", "image", "phone_number", "mobile_number")