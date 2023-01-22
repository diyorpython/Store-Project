from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customuser, Product

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
