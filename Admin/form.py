from django import forms
from .models import customer, Category, Sub_Category, Product, gallery


class UserForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image', 'item']


class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['sub_id', 'image', 'name', 'Category_id']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pro_name', 'file', 'description', 'price', 'discount', 'size', 'colors', 'sub_cat_id']


class galleryForm(forms.ModelForm):
    class Meta:
        model = gallery
        fields = ['gal_id', 'gal_image', 'pro_id']
