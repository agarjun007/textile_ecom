from django.urls import path
from . import views
urlpatterns = [
   
    path('admin/', views.admin_login, name='adminlogin'),
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

    path('adminpanel_colors/', views.admin_panel_colors, name='adminpanelcolors'),
    path('color_validate/', views.color_validate, name='createcolor'),
    path('color_validate/<int:id>', views.color_validate, name='editcolor'),

    path('adminpanel_sizes/', views.admin_panel_sizes, name='adminpanelsizes'),
    path('size_validate/', views.size_validate, name='createsize'),
    path('size_validate/<int:id>', views.size_validate, name='editsize'),

    path('adminpanel_products/', views.admin_panel_products, name='adminpanelproducts'),
    path('create_products/', views.create_products, name='createproducts'),
    path('edit_products/<int:id>', views.edit_products, name='editproducts'),
    path('update_products/<int:id>', views.update_products, name='updateproducts'),
    path('delete_products/<int:id>', views.delete_products, name='deleteproducts'),

 
]
