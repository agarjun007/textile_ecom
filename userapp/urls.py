from django.urls import path
from . import views



urlpatterns = [
    path('', views.guest_home, name='guesthome'),
    path('home/', views.user_home, name='userhome'),
    path('signup/', views.user_signup, name='usersignup'),
    path('signin/', views.user_signin, name='usersignin'),
    path('otplogin/', views.otp_login, name='otplogin'),
    path('verifyotp/', views.verify_otp, name='verifyotp'),

    path('category/<int:id>', views.category,name='category'),  
    path('product_view/<int:id>', views.product_view, name='productview'),
    path('show_cart/', views.show_cart, name='showcart'),

    path('delete_item/<int:id>', views.delete_item, name='deleteitem'),
    path('user_profile/', views.user_profile, name='userprofile'),
    path('user_cart/<int:id>', views.user_cart, name='usercart'),
    path('cart_edit/', views.cart_edit, name='cartedit'),
    path('show_address/', views.show_address, name='showaddress'),
    path('create_address/', views.create_address, name='createaddress'),
    path('edit_address/<int:id>', views.edit_address, name='editaddress'),
    path('user_order_history/', views.user_order_history, name='userorderhistory'),
    path('user_payment/<int:id>', views.user_payment, name='userpayment'),
    path('paypal_payment/', views.paypl_payment, name='paypalpayment'),
    path('razorpay_payment/', views.razorpay_payment, name='razorpaypayment'),
    path('user_logout/', views.user_logout, name='userlogout'),

]