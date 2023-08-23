from django import forms

from django.forms import forms, ModelForm
from client.models import Order,  CartItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user_id', 'item', 'ordered_date', 'ordered']




class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['user_id', 'ordered', 'product_id', 'quantity']

