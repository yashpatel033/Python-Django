from django.db import models
from django.forms import ModelForm
from django_countries.fields import CountryField

from Admin.models import Product, customer


class BillingAdress(models.Model):
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Street_Address = models.CharField(max_length=100)
    Apartment_Address = models.CharField(max_length=100, null=True, blank=True)
    Countries = models.CharField(max_length=50)
    Zip = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12)
    E_mail = models.EmailField()


    def __str__(self):
        return self.user_id.firstname

class CartItem(models.Model):
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product_id.pro_name}"

    def get_total_item_price(self):
        return self.quantity * self.product_id.price


class Order(models.Model):
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    item = models.ManyToManyField(CartItem)
    total_price = models.FloatField()
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_Address = models.ForeignKey(BillingAdress, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_id.firstname

    def total(self):
        return sum(item.get_total_item_price() for item in self.item.all())


class ShippingAddress(models.Model):
    user_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Street_Address = models.CharField(max_length=100, null=True, blank=True)
    Apartment_Address = models.CharField(max_length=100, null=True, blank=True)
    Countries = CountryField(multiple=False, null=True, blank=True)
    Zip = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    E_mail = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user_id.firstname


