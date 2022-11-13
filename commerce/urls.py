from django.urls import path
from . import views
urlpatterns = [
   
    path('admin/', views.admin_login, name='adminlogin'),
    path('admin_logout/', views.admin_logout, name='adminlogout'),
    path('adminpanel/', views.admin_panel, name='adminpanel'),

    path('adminpanel_user/', views.admin_panel_user, name='adminpaneluser'),
    path('user-validate/', views.user_validate, name='create_user'),
    path('user-validate/<int:id>', views.user_validate, name='edit_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    # path('block_user/<int:id>', views.block_user, name='block_user'),

    
    path('adminpanel_category/', views.admin_panel_category, name='adminpanelcategory'),
    path('category-validate/', views.category_validate, name='create_category'),
    path('category-validate/<int:id>', views.category_validate, name='edit_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),

    path('adminpanel_colors/', views.admin_panel_colors, name='adminpanelcolors'),
    path('color-validate/', views.color_validate, name='create_color'),
    path('color-validate/<int:id>', views.color_validate, name='edit_color'),
    path('delete_color/<int:id>', views.delete_color, name='delete_color'),

    path('adminpanel_sizes/', views.admin_panel_sizes, name='adminpanelsizes'),
    path('size-validate/', views.size_validate, name='create_size'),
    path('size-validate/<int:id>', views.size_validate, name='edit_size'),
    path('delete_size/<int:id>', views.delete_size, name='delete_size'),

    path('adminpanel_subproducts/', views.admin_panel_subproducts, name='adminpanelsubproducts'),
    path('subproduct-validate/', views.product_validate, name='create_product'),
    path('product-validate/<int:id>', views.product_validate, name='edit_product'),
    path('delete_products/<int:id>', views.delete_products, name='delete_product'),

    path('adminpanel_products/', views.admin_panel_products, name='adminpanelproducts'),
    path('mainproduct-validate/<int:id>', views.mainproduct_validate, name='edit_main_product'),

 
]
