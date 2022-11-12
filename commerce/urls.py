from django.urls import path
from . import views
urlpatterns = [
   
    path('admin/', views.admin_login, name='adminlogin'),
    path('admin_logout/', views.admin_logout, name='adminlogout'),
    path('adminpanel/', views.admin_panel, name='adminpanel'),

    path('adminpanel_user/', views.admin_panel_user, name='adminpaneluser'),
    path('user-validate/', views.user_validate, name='create_user'),
    path('user-validate/<int:id>', views.user_validate, name='edit_user'),
    path('delete_user/<int:id>', views.delete_user, name='deleteuser'),
    path('block_user/<int:id>', views.block_user, name='block_user'),

    
    path('adminpanel_category/', views.admin_panel_category, name='adminpanelcategory'),
    path('category-validate/', views.category_validate, name='create_category'),
    path('category-validate/<int:id>', views.category_validate, name='edit_category'),
    path('delete_category/<int:id>', views.delete_category, name='deletecategory'),

    path('adminpanel_colors/', views.admin_panel_colors, name='adminpanelcolors'),
    path('color-validate/', views.color_validate, name='create_color'),
    path('color-validate/<int:id>', views.color_validate, name='edit_color'),

    path('adminpanel_sizes/', views.admin_panel_sizes, name='adminpanelsizes'),
    path('size-validate/', views.size_validate, name='create_size'),
    path('size-validate/<int:id>', views.size_validate, name='edit_size'),

    path('adminpanel_products/', views.admin_panel_products, name='adminpanelproducts'),
    path('product-validate/', views.product_validate, name='create_product'),
    path('product-validate/<int:id>', views.product_validate, name='edit_product'),
    path('delete_products/<int:id>', views.delete_products, name='deleteproducts'),

 
]
