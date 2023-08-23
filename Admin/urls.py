from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show),
    path('create_user/', views.create_user),
    path('user_list/', views.user_list),
    path('login/', views.login),
    path('Category/', views.CategoryInsert),
    path('cat_edit/<int:id>', views.cat_edit),
    path('cat_update/<int:id>', views.cat_update),
    path('cat_delete/<int:id>', views.cat_delete),
    path('product_list/', views.product_list),
    path('pro_details/<int:id>/', views.pro_details),
    path('sub_category/', views.sub_category),
    path('sub_edit/<int:id>', views.sub_edit),
    path('sub_update/<int:id>', views.sub_update),
    path('sub_delete/<int:id>', views.sub_delete),
    path('add_pro/', views.add_pro),
    path('pro_edit/<int:id>', views.pro_edit),
    path('pro_update/<int:id>', views.pro_update),
    path('pro_delete/<int:id>', views.pro_delete),
    path('gallery_add/', views.gallery_add),
    path('gal_edit/<int:id>/', views.gal_edit),
    path('gal_update/<int:id>/', views.gal_update),
    path('gal_delete/<int:id>', views.gal_delete),
    path('order_show/', views.order_Show),




]
