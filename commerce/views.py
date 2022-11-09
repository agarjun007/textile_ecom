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
        order = Order.objects.all()
        order_collection = {}
        for order in order:
            if not order.tid in order_collection.keys():
                order_collection[order.tid] = order
        length_order = len(order_collection)
        length_user = len(user)
        length_product = len(product)
        data = [length_product, length_user, length_order]
        return render(request, 'commerce/admin_panel.html',
                      {'table_data': user, 'length_user': length_user, 'length_product': length_product,
                       'length_order': length_order, 'data': data})
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


def create_category(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            category_name = request.POST['categoryname']
            category = Category.objects.create(categoryname=category_name)
            category.save();
            return redirect(admin_panel_category)
        else:
            return render(request, 'commerce/create_category.html')
    else:
        return redirect(admin_login)


def edit_category(request, id):
    if request.session.has_key('password'):
        category_data = Category.objects.get(id=id)
        return render(request, 'commerce/edit_category.html', {'category_data': category_data})
    else:
        return redirect(admin_login)


def update_category(request, id):
    if request.session.has_key('password'):
        if request.method == "POST":
            category_name = request.POST['categoryname']
            category = Category.objects.get(id=id)
            category.categoryname = category_name
            category.save()
            return redirect(admin_panel_category)
        else:
            return render(request, 'commerce/edit_category.html')
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
        product_data = products.objects.all()
        return render(request, 'commerce/adminpanel_products.html', {'table_data': product_data})
    else:
        return redirect(admin_login)


def create_products(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            category_data = Category.objects.get(id=request.POST['category'])
            product_name = request.POST['productname']
            product_desc = request.POST['productdesc']
            price = request.POST['price']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            image_data = request.POST['pro_img']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            print('formatttttt',ext)

            img_decoded = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            product = products.objects.create(category=category_data, productname=product_name,
                                              productdesc=product_desc, price=price, Quantity=quantity,
                                              productimage=img_decoded, unit=unit)
            product.save();
            messages.info(request, "Product created successfully..")
            return redirect(create_products)
        else:
            category_data = Category.objects.all()
            return render(request, 'commerce/create_products.html', {'category_data': category_data})
    else:
        return redirect(admin_login)


def edit_products(request, id):
    if request.session.has_key('password'):
        product = products.objects.get(id=id)
        category_data = Category.objects.all()
        return render(request, 'commerce/edit_products.html', {'category_data': category_data,
                                                               'product_data': product})
    else:
        return redirect(admin_login)


def update_products(request, id):
    if request.session.has_key('password'):
        if request.method == "POST":
            category = Category.objects.get(id=request.POST['category'])
            product_name = request.POST['productname']
            product_desc = request.POST['productdesc']
            price = request.POST['price']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            product = products.objects.get(id=id)
            product.productname = product_name
            product.category.categoryname = category.categoryname
            product.productdesc = product_desc
            product.price = price
            product.Quantity = quantity
            product.unit = unit
            if 'productimage' not in request.POST:
                product_image = request.FILES.get('productimage')
            else:
                product_image = product.productimage
            product.productimage = product_image
            product.save()

            return redirect(admin_panel_products)
        else:

            return render(request, 'commerce/edit_products.html')
    else:
        return redirect(admin_login)


def delete_products(request, id):
    if request.session.has_key('password'):
        product = products.objects.get(id=id)
        product.delete()
        return redirect(admin_panel_products)
    else:
        return redirect(admin_login)


def create_user(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password']
            password2 = request.POST['confirmpassword']
            mobile = request.POST['mobile']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    return redirect('/create_user')
                else:
                    user = User.objects.create_user(first_name=name, username=username,
                                                    email=email, password=password1, last_name=mobile)
                    user.save();
                messages.info(request, "User created successfully..")
                return redirect('/adminpanel')
            else:
                return redirect('/create_user')
        else:
            return render(request, 'commerce/create_user.html')


def edit_user(request, id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        return render(request, 'commerce/edit_user.html', {'user_data': user})
    else:
        return redirect(admin_login)


def update_user(request, id):
    if request.session.has_key('password'):
        if request.method == "POST":
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            user = User.objects.get(id=id)
            user.first_name = name
            user.username = username
            user.email = email
            user.last_name = mobile
            user.save()
            return redirect(admin_panel)
        else:
            return render(request, 'commerce/edit_user.html')
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


def admin_panel_orders(request):
    if request.session.has_key('password'):
        orders = Order.objects.filter(order_status='pending')
        orders_sorted = {}
        for order in orders:
            if not order.tid in orders_sorted.keys():
                orders_sorted[order.tid] = order
                orders_sorted[order.tid].orderprice = order.totalprice
            else:
                orders_sorted[order.tid].orderprice += order.totalprice
        return render(request, 'commerce/adminpanel_orders.html', {'table_data': orders_sorted})
    else:
        return redirect(admin_login)


def admin_panel_suborders(request, status):
    if status == 'Confirmed':
        orders = Order.objects.filter(order_status=status)
        order_sorted = {}
        for order in orders:
            if not order.tid in order_sorted.keys():
                order_sorted[order.tid] = order
                order_sorted[order.tid].orderprice = order.totalprice
            else:
                order_sorted[order.tid].orderprice += order.totalprice

        return render(request, 'commerce/adminpanel_suborders.html', {'table_data': order_sorted, 'heading': status})

    elif status == 'Cancelled':
        orders = Order.objects.filter(order_status=status)
        order_sorted = {}
        for order in orders:
            if not order.tid in order_sorted.keys():
                order_sorted[order.tid] = order
                order_sorted[order.tid].orderprice = order.totalprice
            else:
                order_sorted[order.tid].orderprice += order.totalprice
        return render(request, 'commerce/adminpanel_suborders.html', {'table_data': order_sorted, 'heading': status})


def cancel_order(request, tid):
    if request.session.has_key('password'):
        order = Order.objects.filter(tid=tid)
        for items in order:
            items.order_status = 'Cancelled'
            items.save()
        return redirect(admin_panel_orders)
    else:
        return redirect(admin_login)


def confirm_order(request, tid):
    if request.session.has_key('password'):
        order = Order.objects.filter(tid=tid)
        for items in order:
            items.order_status = 'Confirmed'
            items.save()
        return redirect(admin_panel_orders)
    else:
        return redirect(admin_login)


def admin_panel_reports(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            if 'date_report' in request.POST:
                from_date = request.POST['from']
                to_date = request.POST['to']
                orders = Order.objects.filter(tdate__range=[from_date, to_date])
                order_sorted_tid = {}
                for order in orders:
                    if not order.tid in order_sorted_tid.keys():
                        order_sorted_tid[order.tid] = order
                        order_sorted_tid[order.tid].orderprice = order.totalprice
                        order_sorted_tid[order.tid].total_products = 1
                    else:
                        order_sorted_tid[order.tid].orderprice += order.totalprice
                        order_sorted_tid[order.tid].total_products += 1
                order_sorted_date = {}
                for orders, order_sorted in order_sorted_tid.items():
                    if not order_sorted.tdate in order_sorted_date.keys():
                        order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                                 "total_products": order_sorted.total_products}
                    else:
                        order_sorted_date[order_sorted.tdate]["order_count"] += 1
                        order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                        order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
                return render(request, 'commerce/adminpanel_reports.html', {'table_data': order_sorted_date})
            elif 'category_report' in request.POST:
                report_type = request.POST['report_type']
                if report_type == 'this_day':
                    heading = 'Today'
                    today_date = date.today()
                    orders = Order.objects.filter(tdate=today_date)
                    order_sorted_tid = {}
                    for order in orders:
                        if not order.tid in order_sorted_tid.keys():
                            order_sorted_tid[order.tid] = order
                            order_sorted_tid[order.tid].total_products = 1
                            order_sorted_tid[order.tid].orderprice = order.totalprice
                        else:
                            order_sorted_tid[order.tid].total_products += 1
                            order_sorted_tid[order.tid].orderprice += order.totalprice
                    order_sorted_date = {}
                    for orders, order_sorted in order_sorted_tid.items():
                        if not order_sorted.tdate in order_sorted_date.keys():
                            order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                                     "total_products": order_sorted.total_products}
                        else:
                            order_sorted_date[order_sorted.tdate]["order_count"] += 1
                            order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                            order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
                    return render(request, 'commerce/adminpanel_reports.html',
                                  {'table_data': order_sorted_date, 'heading': heading})

                elif report_type == 'last_7_days':
                    heading = 'Last 7 days'
                    today_date = date.today()
                    last_week_from_date = today_date - timedelta(days=7)
                    orders = Order.objects.filter(tdate__range=[last_week_from_date, today_date])
                    order_sorted_tid = {}
                    for order in orders:
                        if not order.tid in order_sorted_tid.keys():
                            order_sorted_tid[order.tid] = order
                            order_sorted_tid[order.tid].total_products = 1
                            order_sorted_tid[order.tid].orderprice = order.totalprice
                        else:
                            order_sorted_tid[order.tid].total_products += 1
                            order_sorted_tid[order.tid].orderprice += order.totalprice
                    order_sorted_date = {}
                    for orders, order_sorted in order_sorted_tid.items():
                        if not order_sorted.tdate in order_sorted_date.keys():
                            order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                                     "total_products": order_sorted.total_products}
                        else:
                            order_sorted_date[order_sorted.tdate]["order_count"] += 1
                            order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                            order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
                    return render(request, 'commerce/adminpanel_reports.html',
                                  {'table_data': order_sorted_date, 'heading': heading})


                elif report_type == 'this_month':
                    today_date = date.today()
                    month = today_date.strftime('%B')
                    orders = Order.objects.filter(tdate__month=today_date.month)
                    order_sorted_tid = {}
                    for order in orders:
                        if not order.tid in order_sorted_tid.keys():
                            order_sorted_tid[order.tid] = order
                            order_sorted_tid[order.tid].total_products = 1
                            order_sorted_tid[order.tid].orderprice = order.totalprice
                        else:
                            order_sorted_tid[order.tid].total_products += 1
                            order_sorted_tid[order.tid].orderprice += order.totalprice
                    order_sorted_date = {}
                    for orders, order_sorted in order_sorted_tid.items():
                        if not order_sorted.tdate in order_sorted_date.keys():
                            order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                                     "total_products": order_sorted.total_products}
                        else:
                            order_sorted_date[order_sorted.tdate]["order_count"] += 1
                            order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                            order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
                    return render(request, 'commerce/adminpanel_reports.html',
                                  {'table_data': order_sorted_date, 'heading': month})


                elif report_type == 'annual':
                    today_date = date.today()
                    year = today_date.year
                    orders = Order.objects.filter(tdate__year=today_date.year)
                    order_sorted_tid = {}
                    for order in orders:
                        if not order.tid in order_sorted_tid.keys():
                            order_sorted_tid[order.tid] = order
                            order_sorted_tid[order.tid].total_products = 1
                            order_sorted_tid[order.tid].orderprice = order.totalprice
                        else:
                            order_sorted_tid[order.tid].total_products += 1
                            order_sorted_tid[order.tid].orderprice += order.totalprice
                    order_sorted_date = {}
                    for orders, order_sorted in order_sorted_tid.items():
                        if not order_sorted.tdate in order_sorted_date.keys():
                            order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                                     "total_products": order_sorted.total_products}
                        else:
                            order_sorted_date[order_sorted.tdate]["order_count"] += 1
                            order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                            order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
                    return render(request, 'commerce/adminpanel_reports.html',
                                  {'table_data': order_sorted_date, 'heading': year})
        else:
            heading = 'Today'
            today_date = date.today()
            orders = Order.objects.filter(tdate=today_date)
            order_sorted_tid = {}
            for order in orders:
                if not order.tid in order_sorted_tid.keys():
                    order_sorted_tid[order.tid] = order
                    order_sorted_tid[order.tid].total_products = 1
                    order_sorted_tid[order.tid].orderprice = order.totalprice
                else:
                    order_sorted_tid[order.tid].total_products += 1
                    order_sorted_tid[order.tid].orderprice += order.totalprice
            order_sorted_date = {}
            for orders, order_sorted in order_sorted_tid.items():
                if not order_sorted.tdate in order_sorted_date.keys():
                    order_sorted_date[order_sorted.tdate] = {"order_count": 1, "price": order_sorted.orderprice,
                                                             "total_products": order_sorted.total_products}
                else:
                    order_sorted_date[order_sorted.tdate]["order_count"] += 1
                    order_sorted_date[order_sorted.tdate]["price"] += order_sorted.orderprice
                    order_sorted_date[order_sorted.tdate]["total_products"] += order_sorted.total_products
            return render(request, 'commerce/adminpanel_reports.html',
                          {'table_data': order_sorted_date, 'heading': heading})
    else:
        return redirect(admin_login)


def admin_panel_subreports(request, status):
    if status == 'Confirmed':
        orders = Order.objects.filter(order_status=status)
        order_sorted_tid = {}
        for order in orders:
            if not order.tid in order_sorted_tid.keys():
                order_sorted_tid[order.tid] = order
                order_sorted_tid[order.tid].orderprice = order.totalprice
            else:
                order_sorted_tid[order.tid].orderprice += order.totalprice

        return render(request, 'commerce/adminpanel_subreports.html',
                      {'table_data': order_sorted_tid, 'heading': status})

    elif status == 'Cancelled':
        orders = Order.objects.filter(order_status=status)
        order_sorted_tid = {}
        for order in orders:
            if not order.tid in order_sorted_tid.keys():
                order_sorted_tid[order.tid] = order
                order_sorted_tid[order.tid].orderprice = order.totalprice
            else:
                order_sorted_tid[order.tid].orderprice += order.totalprice
        return render(request, 'commerce/adminpanel_subreports.html',
                      {'table_data': order_sorted_tid, 'heading': status})


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(admin_login)
