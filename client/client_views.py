import json
import sys
from datetime import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.template import context
from django.urls import reverse
from django.views import View
from Admin.models import customer, Category, Sub_Category, Product, gallery
from Admin.form import UserForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .form import OrderForm, CartItemForm

'''from .form import orderForm, orderitemForm'''

from .models import CartItem, Order, BillingAdress, ShippingAddress
from .inherit import cartData


def header(request, Category_id):
    cat = Category.objects.get(id=Category_id)
    return render(request, 'client_header.html', {'cat': cat})


def client_index(request):
    cat = Category.objects.all()
    pro = Product.objects.all()
    return render(request, 'client_index.html', {'cat': cat, 'pro': pro})


def client_login(request):
    if request.method == 'POST':
        e = request.POST.get('email')
        p = request.POST.get('password')
        val = customer.objects.filter(email=e, password=p).count()

        if val == 1:
            data = customer.objects.filter(email=e, password=p)
            for items in data:
                request.session['email'] = items.email
                request.session['id'] = items.id
                return redirect('/client/client_index/')

        else:
            messages.error(request, 'Invalid username and password')
            return render(request, 'client_login.html')
    else:

        return render(request, 'client_login.html')


def client_register(request):
    if request.method == 'POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirm_password']
        c = request.POST['contact']
        user = customer(firstname=f, lastname=l,email=e,password=p,confirm_password=cp,contact=c)
        user.save()
        return redirect('/client/client_login/')
    else:
        pass
    return render(request, 'client-register.html')


def logout(request):
    try:
        del request.session['id']
        return redirect('/client/client_login/')
    except:
        return redirect('/client/client_login/')


def client_sub_cat(request, id=0):
    c = Sub_Category.objects.filter(Category_id=id)
    return render(request, 'client-sub-cat.html', {'c': c})


def client_product(request, id=0):
    pro = Product.objects.filter(sub_cat_id=id)
    cat = Sub_Category.objects.all()
    gal = gallery.objects.filter(pro_id=id)
    return render(request, 'client_product.html', {'pro': pro, 'cat': cat, 'gal': gal})


def client_product_details(request, id=0):

    g = gallery.objects.filter(pro_id=id)
    pro = Product.objects.get(id=id)
    return render(request, 'client-product-detail.html', {'pro': pro, 'g': g})


def client_pro_view(request, id=0):
    gal = gallery.objects.filter(pro_id=id)
    pro = Product.objects.all()
    return render(request, 'product-page(vertical-tab).html', {'gal':gal, 'pro':pro})


def add_to_cart(request):
    if request.method == 'POST':
        try:
            u = request.session['id']
            p = request.POST.get('product_id')
            c = request.POST['ordered']
            q = request.POST['quantity']
            cal = CartItem(user_id_id=u, product_id_id=p, ordered=c, quantity=q)
            print('-----', cal)
            cal.save()
            print('-----', cal)
            return redirect('/client/show_cart/')
        except:
            print('---', sys.exc_info())
    return redirect('/client/client_product_details/')


def show_cart(request):
    ids = request.session['id']
    cart = CartItem.objects.filter(user_id=ids)
    pay = Order.objects.all()
    amount = 0.0
    total_amount = 0.0
    shipping_amount = 0.0
    cart_item = [p for p in CartItem.objects.filter(user_id=ids)]
    if cart_item:
        for p in cart_item:
            temp_amount = (p.quantity * p.product_id.price)
            amount += temp_amount
            total_amount = amount + shipping_amount

    return render(request, 'cart.html', {'cart': cart, 'pay': pay, 'total_amount': total_amount})


'''def adjust_cart(request, id):
    cart = request.session.get(id=id)
    quantity = cart[id] - 1
    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(product_id_id=id)
    request.session['show_cart'] = cart
    if not cart:
        return redirect(reverse('/client/client_index'))
    return redirect(reverse('/client/show_cart/'))
'''


def adjust_cart(request, id):
    d = CartItem.objects.get(id=id)
    d.delete()
    return redirect('/client/show_cart/')


def checkout(request):
    e = request.session['id']
    us = customer.objects.get(id=e)
    user = CartItem.objects.filter(user_id=e)
    amount = 0.0
    total_amount = 0.0
    shipping_amount = 0.0
    cart_item = [p for p in CartItem.objects.filter(user_id=e)]
    if cart_item:
        for p in cart_item:
            temp_amount = (p.quantity * p.product_id.price)
            amount += temp_amount
            total_amount = amount + shipping_amount
    if request.method == 'POST':
        try:
            u = request.session['id']
            s = request.POST['Street_Address']
            a = request.POST['Apartment_Address']
            c = request.POST['Countries']
            z = request.POST['Zip']
            city = request.POST['city']
            p = request.POST['phone']
            mail = request.POST['E_mail']

            bill = BillingAdress(user_id_id=u, Street_Address=s, Apartment_Address=a, Countries=c, Zip=z, city=city,
                                 E_mail=mail, phone=p)
            bill.save()
            print("__", bill)
            return redirect('/client/order_summery/')
        except:
            print("___", sys.exc_info())

    return render(request, 'checkout.html', {'user': user, 'us':us,  'amount': amount, 'total_amount': total_amount})


def order_summery(request):
    us = request.session['id']
    bil = BillingAdress.objects.filter(user_id=us)
    cart = CartItem.objects.filter(user_id=us)
    amount = 0.0
    total_amount = 0.0
    shipping_amount = 0.0
    cart_item = [p for p in CartItem.objects.filter(user_id=us)]
    if cart_item:
        for p in cart_item:
            temp_amount = (p.quantity * p.product_id.price)
            amount += temp_amount
            total_amount = amount + shipping_amount
    if request.method == 'POST':
        try:
            u = request.session['id']
            p = request.POST['total_price']
            od = date.today().strftime('%Y-%m-%d')
            sd = date.today().strftime('%Y-%m-%d')
            o = request.POST['ordered']
            bill = request.POST['billing_Address']
            order = Order(user_id_id=u, total_price=p, start_date=sd, ordered_date=od, ordered=o,
                          billing_Address_id=bill)
            print("__", order)
            order.save()
            print("__", order)
            return redirect('/client/payment_done/')
        except:
            print("___", sys.exc_info())
    return render(request, 'order-summery.html', {'us': us, 'bil': bil, 'cart': cart, 'amount': amount, 'total_amount':
        total_amount})


''' if request.method == 'POST':
        try:
            e = request.session['id']
            b = BillingAdress.objects.filter(billing_Address=e)
            d = date.today().strftime('%Y-%m-%d')
            sd = date.today().strftime('%Y-%m-%d')
            ord = request.POST['ordered']
            tp = request.POST['total_price']
            o = Order(user_id_id=e, ordered=ord, ordered_date=d, start_date=sd, billing_Address_id=b,
                          total_price=tp)
            o.save()
            print("___", o)
            return redirect('/client/payment_done/')
        except:
            print("___", sys.exc_info())'''


def payment_done(request):
    e = request.session['id']
    cart = CartItem.objects.filter(user_id=e)
    amount = 0.0
    total_amount = 0.0
    shipping_amount = 0.0
    cart_item = [p for p in CartItem.objects.filter(user_id=e)]
    o = Order.objects.filter(user_id=e)
    ord = Order.objects.get(user_id=e)
    if cart_item:
        for p in cart_item:
            temp_amount = (p.quantity * p.product_id.price)
            amount += temp_amount
            shipping_amount = shipping_amount
            total_amount = amount + shipping_amount

    return render(request, 'order-success.html',
                  {'total_amount': total_amount, 'cart': cart, 'amount': amount, 'shipping_amount': shipping_amount, 'o':o, 'ord':ord})


def order_success(request):
    order = Order.objects.all()
    return render(request, 'order-success.html')
