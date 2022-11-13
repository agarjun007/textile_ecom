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
    path('user_logout/', views.user_logout, name='userlogout'),

    path('get-subproduct/', views.get_subproduct_details, name='get_subproduct_details'),

]