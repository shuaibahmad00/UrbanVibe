from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'), # Default to dashboard
    path('login/', views.admin_login, name='admin_login'),
    path('users/', views.view_users, name='view_users'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.view_products, name='view_products'),
    path('orders/', views.view_orders, name='view_orders'),
    path('sales-report/', views.sales_report, name='sales_report'),
]
