from django.urls import path
from . import views
urlpatterns = [
   
    path('admin_login/', views.admin_login, name='adminlogin'),
    path('admin_logout/', views.admin_logout, name='adminlogout'),
    path('adminpanel/', views.admin_panel, name='adminpanel'),

    path('adminpanel_user/', views.admin_panel_user, name='adminpaneluser'),
    path('create_user/', views.create_user, name='createuser'),
    path('edit_user/<int:id>', views.edit_user, name='edituser'),
    path('update_user/<int:id>', views.update_user, name='updateuser'),
    path('delete_user/<int:id>', views.delete_user, name='deleteuser'),
    path('block_user/<int:id>', views.block_user, name='blockuser'),

    
    path('adminpanel_category/', views.admin_panel_category, name='adminpanelcategory'),
    path('create_category/', views.create_category, name='createcategory'),
    path('edit_category/<int:id>', views.edit_category, name='editcategory'),
    path('update_category/<int:id>', views.update_category, name='updatecategory'),
    path('delete_category/<int:id>', views.delete_category, name='deletecategory'),

    path('adminpanel_products/', views.admin_panel_products, name='adminpanelproducts'),
    path('create_products/', views.create_products, name='createproducts'),
    path('edit_products/<int:id>', views.edit_products, name='editproducts'),
    path('update_products/<int:id>', views.update_products, name='updateproducts'),
    path('delete_products/<int:id>', views.delete_products, name='deleteproducts'),

    path('adminpanel_orders/', views.admin_panel_orders, name='adminpanelorders'),
    path('adminpanel_suborders/<str:status>', views.admin_panel_suborders, name='adminpanelsuborders'),
    path('adminpanel_suborders/<str:status>', views.admin_panel_suborders, name='adminpanelsuborders'),
    path('confirm_order/<str:tid>', views.confirm_order,name='confirmorder'),
    path('cancel_order/<str:tid>', views.cancel_order,name='cancelorder'),

    path('adminpanel_reports/', views.admin_panel_reports, name='adminpanelreports'),
    path('adminpanel_subreports/<str:status>', views.admin_panel_subreports, name='adminpanelsubreports'),

 
]
