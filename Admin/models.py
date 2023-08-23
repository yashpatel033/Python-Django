from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


class customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    is_admin= models.IntegerField(default=0)
    confirm_password = models.CharField(max_length=10)
    contact = models.CharField(max_length=12)

    class Meta:
        db_table = 'User'


class Category(models.Model):
    image = models.FileField()
    item = models.CharField(max_length=50)

    class Meta:
        db_table = 'Category'


class Sub_Category(models.Model):
    sub_id = models.AutoField(primary_key=True)
    image = models.FileField()
    name = models.CharField(max_length=100)
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Sub_Category'


class Product(models.Model):
    COLOR_CHOICES = (
        ('1', 'Black'),
        ('2', 'Blue'),
        ('3', 'Red'),
        ('4', 'White'),
        ('5', 'Yellow'),
        ('6', 'Green'),
        ('7', 'Gray'),
    )
    SIZE_CHOICES =(
        ('1', 'S'),
        ('2', 'M'),
        ('3', 'L'),
        ('4', 'XL'),
        ('5', 'XXL'),
        ('6', 'XXXL'),
    )
    pro_name = models.CharField(max_length=30)
    file = models.FileField()
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField()
    size = MultiSelectField(max_length=200, choices=SIZE_CHOICES, max_choices=5)
    colors = MultiSelectField(max_length=200, choices=COLOR_CHOICES, max_choices=6)
    sub_cat_id = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Product'


class gallery(models.Model):
    gal_id = models.AutoField(primary_key=True)
    gal_image = models.FileField()
    pro_id = models.ForeignKey(Product, on_delete=models.CASCADE)

