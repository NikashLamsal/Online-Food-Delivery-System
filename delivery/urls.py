from django.urls import path
from . import views


app_name = 'delivery'

urlpatterns = [
    
    path("",views.home,name='home'),

    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('customers/', views.customer_list, name='customer_list'),

    path('analytics/', views.analytics, name='analytics'),
    path('sql-demo/', views.sql_queries_demo, name='sql_demo'),


    path('api/restaurant/<int:restaurant_id>/menu/', views.api_restaurant_menu, name='api_restaurant_menu'),
    path('api/order/<int:order_id>/status/', views.api_order_status, name='api_order_status'),
    
]