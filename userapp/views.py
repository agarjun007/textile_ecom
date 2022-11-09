from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
import datetime
from commerce.models import *
from .models import *
from django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File
import razorpay
import requests
import json


def user_signup(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        mobile = request.POST['mobile']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return JsonResponse('usernamemismatch', safe=False)
            else:
                user = User.objects.create_user(first_name=name, username=username, email=email, password=password1,
                                                last_name=mobile, is_active=True)
                user.save();
            return JsonResponse('valid', safe=False)
        else:
            return JsonResponse('invalid', safe=False)
            messages.info(request, "password not match")
    else:
        return render(request, 'userapp/signup.html')


def user_signin(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()

        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                return JsonResponse('blocked', safe=False)
            else:
                auth.login(request, user)
                return JsonResponse('valid', safe=False)
        else:
            return JsonResponse('invalid', safe=False)
    else:

        return render(request, 'userapp/user_signin.html')


def otp_login(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        if User.objects.filter(last_name=mobile).exists():
            user = User.objects.get(last_name=mobile)
            if user.is_active:
                mobile = str(91) + mobile
                request.session['mobile'] = mobile
                url = "https://d7networks.com/api/verifier/send"

                payload = {'mobile': mobile,
                           'sender_id': 'SMSINFO',
                           'message': 'Your otp code is {code}',
                           'expiry': '9000'}
                files = [

                ]
                headers = {
                    'Authorization': 'Token 4dc831ffc708d93a7287b8846ab5034db634afe0'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)

                print(response.text.encode('utf8'))
                data = response.text.encode('utf8')
                otp_data = json.loads(data.decode('utf-8'))

                otp_id = otp_data['otp_id']
                request.session['id'] = otp_id

                return JsonResponse('valid', safe=False)
            else:
                return JsonResponse('blocked', safe=False)

        else:
            return JsonResponse('invalid', safe=False)
    else:
        otpfield = 0
        return render(request, 'userapp/otp_signin.html', {'otpfield': otpfield})


def verify_otp(request):
    if request.session.has_key('id'):
        if request.method == 'POST':
            otp = request.POST['otp']
            otp_id = request.session['id']

            url = "https://d7networks.com/api/verifier/verify"

            payload = {'otp_id': otp_id,
                       'otp_code': otp}
            files = [

            ]
            headers = {
                'Authorization': 'Token 4dc831ffc708d93a7287b8846ab5034db634afe0'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            data = response.text.encode('utf8')
            otp_data = json.loads(data.decode('utf-8'))
            status = otp_data['status']

            if status == 'success':
                mobile = request.session['mobile']
                mobile_number = str(mobile)
                mobile_number = mobile_number[-10:]
                user = User.objects.filter(last_name=mobile_number).first()
                if user is not None:
                    if user.is_active == False:
                        del request.session['id']
                        return JsonResponse('blocked', safe=False)
                    else:
                        auth.login(request, user)
                        return JsonResponse('valid', safe=False)
                else:
                    del request.session['id']
                    return JsonResponse('invalid', safe=False)

            else:
                del request.session['id']
                return JsonResponse('otp_mismatch', safe=False)

        else:
            otpfield = 1
            return render(request, 'userapp/otp_signin.html', {'otpfield': otpfield})
    else:
        return redirect(user_signin)


def user_home(request):
    if request.user.is_authenticated:
        product = products.objects.all()
        category = Category.objects.all()
        user = request.user
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        return render(request, 'userapp/user_home.html',
                      {'product_data': product, 'category_data': category, 'no': item_count})
    else:
        return redirect(user_signin)


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            cart = Cart.objects.filter(user=user)
            user.first_name = request.POST['name']
            user.last_name = request.POST['mobile']
            user.email = request.POST['email']
            user.save()

            if Userprofile.objects.filter(user=user).exists():
                user_details = Userprofile.objects.get(user=user)

                if 'profile-image-upload' not in request.POST:
                    profile_pic = request.FILES.get('profile-image-upload')
                else:
                    profile_pic = user_details.profilepic

                user_details.profilepic = profile_pic
                user_details.save()
            else:
                profile_pic = request.FILES.get('profile-image-upload')
                Userprofile.objects.create(user=user, profilepic=profile_pic)

            return redirect(user_home)
        else:
            category = Category.objects.all()
            user = request.user
            cart = Cart.objects.filter(user=user)
            item_count = cart.count()
            if Userprofile.objects.filter(user=user).exists():
                user_details = Userprofile.objects.get(user=user)
                return render(request, 'userapp/user_profile.html',
                              {'category_data': category, 'no': item_count, 'userdetails': user_details})
            else:

                return render(request, 'userapp/user_profile.html', {'category_data': category, 'no': item_count})
    else:
        return redirect(user_signin)


def category(request, id):
    product = products.objects.filter(category=id)
    category = Category.objects.all()
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        return render(request, 'userapp/user_home.html',
                      {'product_data': product, 'category_data': category, 'no': item_count})
    else:
        return render(request, 'userapp/guest_home.html', {'product_data': product, 'category_data': category})


def guest_home(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    product = products.objects.all()
    category = Category.objects.all()

    return render(request, 'userapp/guest_home.html',
                  {'product_data': product, 'category_data': category, 'guest': 'Guest'})


def product_view(request, id):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        category = Category.objects.all()
        product = products.objects.get(id=id)
        return render(request, 'userapp/user_product_view.html',
                      {'product_data': product, 'category_data': category, 'no': item_count})
    else:
        category = Category.objects.all()
        product = products.objects.get(id=id)
        return render(request, 'userapp/guest_product_view.html',
                      {'product_data': product, 'category_data': category, 'guest': 'Guest'})


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        grandtotal = 0
        for item in cart:
            item.totalprice = item.quantity * item.product.price
            grandtotal = grandtotal + item.totalprice
        category = Category.objects.all()
        item_count = cart.count()
        if item_count == 0:
            return render(request, 'userapp/user_cart.html', {'category_data': category, 'no': item_count})
        else:
            return render(request, 'userapp/user_cart.html',
                          {'cart_data': cart, 'category_data': category, 'no': item_count, 'grandtotal': grandtotal})

    else:
        return redirect(user_signin)


def delete_item(request, id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(id=id)
        cart.delete()
        return redirect(show_cart)
    else:
        return redirect(guest_home)


def user_cart(request, id):
    if request.user.is_authenticated:
        product = products.objects.get(id=id)
        user = request.user
        if Cart.objects.filter(product=product,user=user).exists():
            cart = Cart.objects.get(product=product,user=user)
            if cart.quantity + 1 <= cart.product.Quantity:
                cart.quantity = cart.quantity + 1
                cart.totalprice = cart.product.price * cart.quantity
                cart.save()
                return redirect(user_home)
            else:
                messages.error(request,'selected quantity is not available for this product')
                return redirect(guest_home)
        else:
            quantity = 1

            Cart.objects.create(user=user, product=product, quantity=quantity)
            return redirect(user_home)
    else:
        return redirect(guest_home)


def cart_edit(request):
    id = request.POST["id"]
    count = 1
    grandtotal = 0
    cart = Cart.objects.filter(user=request.user)
    item = Cart.objects.get(id=id)
    if request.POST["value"] == "add":
        if item.product.Quantity < item.quantity + count:
            return JsonResponse({'total': None, 'grandtotal': None, 'status':0}, safe=False)
        item.quantity = item.quantity + count
        item.save()
        price = item.product.price * item.quantity

        for item in cart:
            grandtotal = grandtotal + item.product.price * item.quantity
    elif request.POST["value"] == "sub":
        item.quantity = item.quantity - count
        item.save()
        price = item.product.price * item.quantity

        for item in cart:
            grandtotal = grandtotal + item.product.price * item.quantity
    return JsonResponse({'total': price, 'grandtotal': grandtotal,'status':1}, safe=False)


def show_address(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        category = Category.objects.all()
        item_count = cart.count()
        address = Address.objects.filter(user=user)
        return render(request, 'userapp/user_address.html',
                      {'category_data': category, 'no': item_count, 'address': address})
    else:
        return redirect(guest_home)


def create_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            name = request.POST['firstname']
            email = request.POST['email']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            Address.objects.create(user=user, name=name, email=email, address=address, city=city,
                                   state=state, pincode=pincode)
            return redirect(show_address)
        else:
            return render(request, 'userapp/edit_address.html')
    else:
        return redirect(guest_home)


def edit_address(request, id):
    if request.user.is_authenticated:
        address_details = Address.objects.get(id=id)
        if request.method == 'POST':
            address_details.name = request.POST['firstname']
            address_details.email = request.POST['email']
            address_details.address = request.POST['address']
            address_details.city = request.POST['city']
            address_details.state = request.POST['state']
            address_details.pincode = request.POST['pincode']
            address_details.save()
            print(address_details.email)
            return redirect(show_address)
        else:
            edit = 1
            return render(request, 'userapp/edit_address.html', {'address': address_details, 'edit': edit})
    else:
        return redirect(guest_home)


def user_order_history(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        category = Category.objects.all()
        cart = Cart.objects.filter(user=user)
        item_count = cart.count()
        return render(request, 'userapp/user_order_history.html',
                      {'items_data': order, 'category_data': category, 'no': item_count})


def user_payment(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            address = Address.objects.get(id=id)
            grandtotal = 0
            date = datetime.datetime.now()
            trans_id = datetime.datetime.now().timestamp()
            mode = request.POST['mode']
            address.name = request.POST['name']
            address.email = request.POST['email']
            address.addrees = request.POST['address']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.pincode = request.POST['pincode']
            address.save()
            cart = Cart.objects.filter(user=user)
            status = 'pending'
            for item in cart:
                item.totalprice = item.quantity * item.product.price
                grandtotal = grandtotal + item.totalprice

            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                     quantity=item.quantity,
                                     totalprice=item.product.price * item.quantity, tdate=date,
                                     tid=trans_id, payment_mode=mode, order_status='pending',
                                     payment_status=status)
                item.product.Quantity = item.product.Quantity - item.quantity
                item.product.save()
            cart.delete()
            if mode == 'COD':
                mode = 'COD'
                messages.info(request, "Order placed Succesfully")
                return JsonResponse({'mode': mode, 'tid': trans_id}, safe=False)

            elif mode == 'Paypal':
                mode = 'Paypal'
                return JsonResponse({'mode': mode, 'tid': trans_id}, safe=False)

            elif mode == 'Razorpay':
                order_amount = grandtotal * 100
                order_currency = 'INR'
                client = razorpay.Client(auth=('rzp_test_EJQneGlqu2SpAQ', 'oCisVDcytFHu60u7EGuzrinD'))
                client.order.create(
                    {'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
                mode = 'Razorpay'
                return JsonResponse({'mode': mode, 'tid': trans_id}, safe=False)
        else:
            user = request.user
            address = Address.objects.filter(id=id)
            cart = Cart.objects.filter(user=user)
            item_count = cart.count()
            grandtotal = 0
            for item in cart:
                item.totalprice = item.quantity * item.product.price
                grandtotal = grandtotal + item.totalprice
            razorpay_total = grandtotal * 100
            return render(request, 'userapp/user_payment.html',
                          {'cart_data': cart, 'no': item_count, 'grandtotal': grandtotal, 'address': address,
                           'razorpay_total': razorpay_total})
    else:
        return redirect(guest_home)


def paypl_payment(request):
    transaction_id = request.POST['tid']
    orders = Order.objects.filter(tid=transaction_id)
    for order in orders:
        order.payment_status = 'SUCCESS'
        order.save()
    return JsonResponse('success', safe=False)


def razorpay_payment(request):
    transaction_id = request.POST['tid']
    orders = Order.objects.filter(tid=transaction_id)
    for order in orders:
        order.payment_status = 'SUCCESS'
        order.save()
    return JsonResponse('success', safe=False)


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(user_signin)
