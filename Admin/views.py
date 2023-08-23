import sys
from django.http import HttpResponse
from django.contrib import messages

from client.models import Order, CartItem
from .models import customer, Category, Sub_Category, Product, gallery
from django.shortcuts import render, redirect
from .form import UserForm, CategoryForm, Sub_CategoryForm, ProductForm, galleryForm
from .functions import handle_uploaded_file
from .models import Product


def dashboard(request):
    o = Order.objects.all().count()
    pro = Product.objects.all().count()
    return render(request, 'index.html', {'o': o, 'pro': pro})


def show(request):
    e = request.session['id']
    ord = Order.objects.all()
    crt = CartItem.objects.filter(user_id=e)
    return render(request, 'index.html', {'ord': ord, 'crt': crt})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/user_list/')
            except:
                print('---', sys.exc_info())
        else:
            pass
    else:
        form = UserForm()
    return render(request, 'create-user.html', {'form': form})


def user_list(request):
    u = customer.objects.all()
    return render(request, 'user-list.html', {'u': u})


def login(request):
    if request.method == 'POST':
        e = request.POST.get('email')
        p = request.POST.get('password')

        val = customer.objects.filter(email=e, password=p, is_admin=1).count()

        if val == 1:
            data = customer.objects.filter(email=e, password=p)
            for items in data:
                request.session['email'] = items.email
                request.session['id'] = items.id
                return redirect('/show/')

        else:
            messages.error(request, 'Invalid username and password')
        return render(request, 'login.html')
    else:

        return render(request, 'login.html')


def CategoryInsert(request):
    b = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['image'])
                form.save()
                return redirect('/Category/')
            except:
                print('---', sys.exc_info())
        else:
            pass
    else:
        form = CategoryForm()

    return render(request, 'category.html', {'form': form, 'b': b})


def cat_edit(request, id):
    b = Category.objects.get(id=id)
    return render(request, 'edit.html', {'b': b})


def cat_update(request, id):
    b = Category.objects.get(id=id)
    form = CategoryForm(request.POST, request.FILES, instance=b)
    if form.is_valid():
        handle_uploaded_file(request.FILES['image'])
        form.save()
        return redirect('/Category/')

    return render(request, 'edit.html', {'b': b})


def cat_delete(request, id):
    d = Category.objects.get(id=id)
    d.delete()
    return redirect('/Category/')


def product_list(request):
    b = Product.objects.all()
    return render(request, 'product-list.html', {'b': b})


def pro_details(request, id):
    pro = Product.objects.get(id=id)
    return render(request, 'product-detail.html', {'pro': pro})


def sub_category(request):
    b = Sub_Category.objects.all()
    c = Category.objects.all()
    if request.method == 'POST':
        form = Sub_CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            print('====================', form)
            try:
                handle_uploaded_file(request.FILES['image'])
                form.save()
                print('---------', form)
                return redirect('/sub_category/')
            except:
                print('---', sys.exc_info())
        else:
            pass
    else:
        form = Sub_CategoryForm()

    return render(request, 'category-sub.html', {'form': form, 'b': b, 'c': c})


def sub_edit(request, id):
    c = Sub_Category.objects.get(sub_id=id)
    return render(request, 'sub-edit.html', {'c': c})


def sub_update(request, id):
    c = Sub_Category.objects.get(sub_id=id)
    form = Sub_CategoryForm(request.POST, request.FILES, instance=c)
    if form.is_valid():
        handle_uploaded_file(request.FILES['image'])
        form.save()
        return redirect('/sub_category/')

    return render(request, 'sub-edit.html', {'c': c})


def sub_delete(request, id):
    d = Sub_Category.objects.get(sub_id=id)
    d.delete()
    return redirect('/sub_category/')


def add_pro(request):
    c = Sub_Category.objects.all()
    p = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print('__', form)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'])
                form.save()
                print('---', form)
                return redirect('/product_list/')
            except:

                print('---', sys.exc_info())
        else:
            pass
    else:

        form = ProductForm()

    return render(request, 'add-product.html', {'form': form, 'c': c, 'p': p})


def pro_edit(request, id):
    c = ProductForm.objects.get(id=id)
    return render(request, 'sub-edit.html', {'g': c})


def pro_update(request, id):
    c = Product.objects.get(id=id)
    form = ProductForm(request.POST, request.FILES, instance=c)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        form.save()
        return redirect('/add_pro/')

    return render(request, 'pro-edit.html', {'c': c})


def pro_delete(request, id):
    d = Product.objects.get(id=id)
    d.delete()
    return redirect('/add_pro/')


def gallery_add(request):
    g = gallery.objects.all()
    c = Product.objects.all()
    if request.method == 'POST':
        form = galleryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['gal_image'])
                form.save()
                print('---------', form)
                return redirect('/gallery_add/')
            except:
                print('---', sys.exc_info())
        else:
            pass
    else:
        form = galleryForm()

    return render(request, 'gallery.html', {'form': form, 'c': c, 'g': g})


def gal_edit(request, id):
    g = gallery.objects.get(gal_id=id)
    return render(request, 'gal-edit.html', {'g': g})


def gal_update(request, id):
    g = gallery.objects.get(gal_id=id)
    form = galleryForm(request.POST, request.FILES, instance=g)
    if form.is_valid():
        handle_uploaded_file(request.FILES['gal_image'])
        form.save()
        return redirect('/gallery_add/')

    return render(request, 'gal-edit.html', {'g': g})


def gal_delete(request, id):
    d = gallery.objects.get(gal_id=id)
    d.delete()
    return redirect('/gallery_add/')


def order_Show(request):
    e = request.session['id']
    ord = Order.objects.all()
    crt = CartItem.objects.filter(user_id=e)
    return render(request, 'order.html', {'ord': ord, 'crt': crt})
