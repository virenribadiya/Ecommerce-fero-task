from django.urls import path
from .views import (CustomerList, CustomerDetail, ProductList, OrderList, OrderDetail)

urlpatterns = [
    path('customers/',CustomerList.as_view(),name='customer_list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer_detail'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('orders/', OrderList.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
]