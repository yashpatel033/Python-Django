from django.urls import path
from . import client_views

urlpatterns = [
    path('client_index/', client_views.client_index),
    path('client_login/', client_views.client_login),
    path('logout/', client_views.logout),
    path('client_register/', client_views.client_register),
    path('header/', client_views.header),
    path('client_sub_cat/<int:id>/', client_views.client_sub_cat),
    path('client_product/<int:id>/', client_views.client_product),
    path('client_product_details/<int:id>/', client_views.client_product_details),
    path('add_to_cart/', client_views.add_to_cart),
    path('show_cart/', client_views.show_cart),
    path('adjust_cart/<int:id>/', client_views.adjust_cart),
    path('checkout/', client_views.checkout),
    path('order_summery/', client_views.order_summery),
    path('payment_done/', client_views.payment_done),
    path('order_success/', client_views.order_success),
    path('client_pro_view/', client_views.client_pro_view)


]
