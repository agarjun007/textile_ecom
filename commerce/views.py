from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import products, Category
from django.http import JsonResponse
from django.http import HttpResponse
from userapp.models import *
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File
from datetime import date, datetime, timedelta


def admin_login(request):
    if request.session.has_key('password'):
        return redirect(admin_panel)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == 'admin':
            request.session['password'] = password
            return JsonResponse('valid', safe=False)

        else:
            return JsonResponse('invalid', safe=False)

    else:
        return render(request, 'commerce/admin_login.html')


def admin_panel(request):
    if request.session.has_key('password'):
        user = User.objects.all()
        product = products.objects.all()
        # order = Order.objects.all()
        # order_collection = {}
        # for order in order:
        #     if not order.tid in order_collection.keys():
        #         order_collection[order.tid] = order
        # length_order = len(order_collection)
        length_user = len(user)
        length_product = len(product) 
        data = [length_product, length_user]
        return render(request, 'commerce/admin_panel.html',
                      {'table_data': user, 'length_user': length_user, 'length_product': length_product,
                       'length_order': None, 'data': data})
    else:
        return redirect(admin_login)


def admin_panel_user(request):
    if request.session.has_key('password'):
        user = User.objects.all()
        return render(request, 'commerce/adminpanel_user.html', {'table_data': user})
    else:
        return redirect(admin_login)


def admin_panel_category(request):
    if request.session.has_key('password'):
        categories = Category.objects.all()
        for category in categories:
            total_items = products.objects.filter(category=category)
            category.productcount = total_items.count()
        return render(request, 'commerce/adminpanel_category.html', {'table_data': categories})
    else:
        return redirect(admin_login)


def category_validate(request,id=None):
    if request.session.has_key('password'):
        if id:                
            category = Category.objects.get(id=id)
            if request.method == "POST":
                category_name = request.POST['categoryname']
                category.categoryname = category_name
                category.save()
                return redirect(admin_panel_category)
            else:
                return render(request, 'commerce/category_validate.html',{'category_data': category})
        else:
            if request.method == 'POST':
                category_name = request.POST['categoryname']
                Category.objects.get_or_create(categoryname=category_name)
                return redirect(admin_panel_category)
            else:
                return render(request, 'commerce/category_validate.html')
        
    else:
        return redirect(admin_login)

def admin_panel_colors(request):
    if request.session.has_key('password'):
        colors = Color.objects.all()
        return render(request, 'commerce/adminpanel_color.html', {'table_data': colors})
    else:
        return redirect(admin_login)

def color_validate(request, id=None):
    if request.session.has_key('password'):
        if id:
            color = Color.objects.get(id=id)
            if request.method == "POST":
                color_name = request.POST['colorname']
                code = request.POST['code']
                color.name = color_name
                color.color_code = code
                color.save()
                return redirect(admin_panel_colors)
            else:
                return render(request, 'commerce/color_validate.html',{'color':color})
        else:
            if request.method == "POST":
                color_name = request.POST['colorname']
                code = request.POST['code']
                Color.objects.get_or_create(name = color_name,color_code = code)
                return redirect(admin_panel_colors)
            else:
                return render(request, 'commerce/color_validate.html')
    else:
        return redirect(admin_login)

def admin_panel_sizes(request):
    if request.session.has_key('password'):
        sizes = Size.objects.all()
        return render(request, 'commerce/adminpanel_size.html', {'table_data': sizes})
    else:
        return redirect(admin_login)

def size_validate(request, id=None):
    if request.session.has_key('password'):
        if id:
            size = Size.objects.get(id=id)
            if request.method == "POST":
                size_name = request.POST['sizename']
                size.name = size_name
                size.save()
                return redirect(admin_panel_sizes)
            else:
                return render(request, 'commerce/size_validate.html',{'size':size})
        else:
            if request.method == "POST":
                size_name = request.POST['sizename']
                Size.objects.get_or_create(name = size_name)
                return redirect(admin_panel_sizes)
            else:
                return render(request, 'commerce/size_validate.html')
    else:
        return redirect(admin_login)

def delete_category(request, id):
    if request.session.has_key('password'):
        category_data = Category.objects.get(id=id)
        category_data.delete()
        return redirect(admin_panel_category)
    else:
        return redirect(admin_login)


def admin_panel_products(request):
    if request.session.has_key('password'):
        product_data = ProductBatch.objects.all()
        return render(request, 'commerce/adminpanel_products.html', {'table_data': product_data})
    else:
        return redirect(admin_login)

def product_validate(request, id=None):
    if request.session.has_key('password'):
        sizes = Size.objects.all()
        colors = Color.objects.all()
        products_data = products.objects.all()
        category_data = Category.objects.all()
        if id:
            product_batch = ProductBatch.objects.get(id=id)
            if request.method == "POST":
                category_id = request.POST['category']
                product_name = request.POST['productname']
                product_desc = request.POST['productdesc']
                price = request.POST['price']
                quantity = request.POST['quantity']
                parent_product = request.POST.get('parent_product')
                unit = request.POST['unit']
                size = request.POST['size']
                color = request.POST['color']
                embroidery = request.POST['embroidery']
                if embroidery == '1':
                    emb_price = request.POST['emb_price']
                else:
                    emb_price = 0
                if parent_product == '0':
                    default = True
                    category = Category.objects.get(id=category_id)
                    product = products.objects.create(productdesc = product_desc,productname = product_name,category = category)
                else:
                    default = True
                    product = products.objects.get(id=parent_product)
                product_batch.product = product
                product_batch.embroidery = True if embroidery == '1' else False
                product_batch.emb_price = emb_price
                product_batch.default = default
                product_batch.size_id = size
                product_batch.color_id = color
                product_batch.price = price
                product_batch.quantity = quantity
                product_batch.unit = unit
                if 'productimage' in request.FILES:
                    image,created = ProductImages.objects.get_or_create(product_batch = product_batch)
                    image.productimage = request.FILES.get('productimage')
                    image.save()
                else:
                    pass
                product_batch.save()
                return redirect(admin_panel_products)
            else:
                return render(request, 'commerce/product_validate.html',{'product_data':product_batch,
                'size_data':sizes,'color_data':colors,'products_data':products_data,'category_data':category_data})
        
        else:
            if request.method == "POST":
                print(request.POST)
                category_id = request.POST['category']
                product_name = request.POST['productname']
                product_desc = request.POST['productdesc']
                price = request.POST['price']
                quantity = request.POST['quantity']
                parent_product = request.POST.get('parent_product','0')
                unit = request.POST['unit']
                size = request.POST['size']
                color = request.POST['color']
                embroidery = request.POST['embroidery']
                if embroidery == '1':
                    emb_price = request.POST['emb_price']
                else:
                    emb_price = 0
                if parent_product == '0':
                    default = True
                    category = Category.objects.get(id=category_id)
                    product = products.objects.create(productdesc = product_desc,productname = product_name,category = category)
                else:
                    default = False
                    product = products.objects.get(id=parent_product)
                product_batch = ProductBatch()
                product_batch.product = product
                product_batch.embroidery = True if embroidery == '1' else False
                product_batch.emb_price = emb_price
                product_batch.default = default
                product_batch.size_id = size
                product_batch.color_id = color
                product_batch.price = price
                product_batch.quantity = quantity
                product_batch.unit = unit
                product_batch.save()
                if 'productimage' in request.FILES:
                    image,created = ProductImages.objects.get_or_create(product_batch = product_batch)
                    image.productimage = request.FILES.get('productimage')
                    image.save()
                else:
                    pass
    
                return redirect(admin_panel_products)
            else:
                return render(request, 'commerce/product_validate.html',{'size_data':sizes,'color_data':colors,
                'products_data':products_data,'category_data':category_data})
    else:
        return redirect(admin_login)


def delete_products(request, id):
    if request.session.has_key('password'):
        product = products.objects.get(id=id)
        product.delete()
        return redirect(admin_panel_products)
    else:
        return redirect(admin_login)


def user_validate(request,id=None):
    if request.session.has_key('password'):
        if id:
            user = User.objects.get(id=id)
            if request.method == "POST":
                name = request.POST['name']
                # username = request.POST['username']
                email = request.POST['email']
                mobile = request.POST['mobile']
                user.first_name = name
                # user.username = username
                user.email = email
                user.last_name = mobile
                user.save()
                return redirect(admin_panel)
            else:
                return render(request, 'commerce/user_validate.html',{'user_data': user})
        else:
            if request.method == 'POST':
                name = request.POST['name']
                username = request.POST['username']
                email = request.POST['email']
                password1 = request.POST['password']
                password2 = request.POST['confirmpassword']
                mobile = request.POST['mobile']

                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        return redirect('create_user')
                    else:
                        user = User.objects.create_user(first_name=name, username=username,
                                                        email=email, password=password1, last_name=mobile)
                    messages.info(request, "User created successfully..")
                    return redirect('/adminpanel')
                else:
                    return redirect('create_user')
            else:
                return render(request, 'commerce/user_validate.html')
    else:
        return redirect(admin_login)


def block_user(request, id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
            user.save()

        else:
            user.is_active = True
            user.save()
        return redirect(admin_panel_user)
    else:
        return redirect(admin_login)


def delete_user(request, id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        user.delete()
        return redirect(admin_panel)
    else:
        return redirect(admin_login)


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(admin_login)
