from django.shortcuts import render, get_object_or_404
from .models import Customer, Restaurant, MenuItem, Order, OrderItem, DeliveryPersonnel
from django.db.models import Count, Sum, Avg, Q
from django.http import JsonResponse
from django.db import connection

# Create your views here.


""" HOME VIEW """
def home(request):
    active_orders_count = Order.objects.exclude(
        status__in=['Delivered', 'Cancelled']
    ).count()

    context = {
        'total_customers': Customer.objects.count(),
        'total_restaurants': Restaurant.objects.count(),
        'total_orders': Order.objects.count(),
        'total_menu_items': MenuItem.objects.count(),
        'active_orders': active_orders_count,
        'recent_orders': Order.objects.select_related('customer', 'restaurant').order_by('-order_date')[:5],
    }
    
    return render(request,'delivery/home.html',context)


""" RESTAURANT VIEW """
def restaurant_list(request):
    restaurants = Restaurant.objects.prefetch_related('menu_items').annotate(
    total_orders= Count('orders'),
    total_revenue= Sum('orders__total_amount')
    ).order_by('-rating')


    context = {
        'restaurants': restaurants
    }
    return render(request, 'delivery/restaurants.html', context)

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
    menu_items = restaurant.menu_items.filter(is_available=True)

    
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items
    }

    return render(request, 'delivery/restaurant_detail.html', context) 

""" ORDERS VIEW """
def order_list(request):

    orders = Order.objects.select_related(
        'customer', 'restaurant', 'delivery_person'
    ).prefetch_related('order_items__menu_item').order_by('-order_date')

    status_filter = request.GET.get('status')
    if status_filter:
            orders = orders.filter(status=status_filter)
        
    context = {
            'orders': orders,
            'status_filter': status_filter
    }
    return render(request, 'delivery/orders.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer', 'restaurant', 'delivery_person'),
        order_id=order_id
    )

    order_items = order.order_items.select_related('menu_item')
    context = {
        'order': order,
        'order_items': order_items
    }  

    return render(request, 'delivery/order_detail.html', context)


""" CUSTOMERS VIEW """
def customer_list(request):
    customers = Customer.objects.annotate(
        total_orders=Count('orders'),
        total_spent=Sum('orders__total_amount') # note for myself - __ is the seperator or syntax for spanning relationship orders __ total_amount isspecific field inside the order 
    ).order_by('-total_spent')
     

    context = {
         
        'customers': customers
    }
    return render(request, 'delivery/customers.html', context)


""" ANALYTICS / REPORTS VIEW """
def analytics(request):

    
    orders_by_status = Order.objects.values('status').annotate(
        count=Count('order_id'),
        revenue=Sum('total_amount')
    ).order_by('-count')
    
    top_restaurants = Restaurant.objects.annotate(
        total_orders=Count('orders'),
        total_revenue=Sum('orders__total_amount'),
        avg_order=Avg('orders__total_amount')
    ).filter(total_orders__gt=0).order_by('-total_revenue')[:5]
    
    popular_items = MenuItem.objects.annotate(
        times_ordered=Count('order_items'),
        total_quantity=Sum('order_items__quantity')
    ).filter(times_ordered__gt=0).order_by('-times_ordered')[:10]
    
    delivery_stats = DeliveryPersonnel.objects.annotate(
        total_deliveries=Count('orders'),
        completed=Count('orders', filter=Q(orders__status='Delivered'))
    ).order_by('-total_deliveries')
    
    context = {
        'orders_by_status': orders_by_status,
        'top_restaurants': top_restaurants,
        'popular_items': popular_items,
        'delivery_stats': delivery_stats
    }
    return render(request, 'delivery/analytics.html', context)




def sql_queries_demo(request):

    with connection.cursor() as cursor:
        
        cursor.execute("""
            SELECT 
                o.order_id,
                c.name AS customer_name,
                r.name AS restaurant_name,
                o.total_amount,
                o.status
            FROM order_table o
            INNER JOIN customer c ON o.customer_id = c.customer_id
            INNER JOIN restaurant r ON o.restaurant_id = r.restaurant_id
            ORDER BY o.order_date DESC
            LIMIT 10
        """)
        inner_join_results = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                mi.name AS item_name,
                r.name AS restaurant_name,
                COUNT(oi.order_item_id) AS times_ordered
            FROM menu_item mi
            LEFT JOIN order_item oi ON mi.item_id = oi.menu_item_id
            LEFT JOIN restaurant r ON mi.restaurant_id = r.restaurant_id
            GROUP BY mi.item_id, mi.name, r.name
            ORDER BY times_ordered DESC
            LIMIT 10
        """)
        left_join_results = cursor.fetchall()

        cursor.execute("""
            SELECT 
                status,
                COUNT(*) AS order_count,
                SUM(total_amount) AS total_revenue
            FROM order_table
            GROUP BY status
        """)
        aggregate_results = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                c.name AS customer_name,
                c.email
            FROM customer c
            WHERE c.customer_id IN (
                SELECT DISTINCT o.customer_id
                FROM order_table o
                INNER JOIN restaurant r ON o.restaurant_id = r.restaurant_id
                WHERE r.rating > 4.0
            )
            LIMIT 10
        """)
        subquery_results = cursor.fetchall()
    
    context = {
        'inner_join_results': inner_join_results,
        'left_join_results': left_join_results,
        'aggregate_results': aggregate_results,
        'subquery_results': subquery_results
    }
    return render(request, 'delivery/sql_demo.html', context)


def api_restaurant_menu(request, restaurant_id):

    menu_items = MenuItem.objects.filter(
        restaurant_id=restaurant_id,
        is_available=True
    ).values('item_id', 'name', 'price', 'category', 'description')
    
    return JsonResponse({
        'success': True,
        'menu_items': list(menu_items)
    })


def api_order_status(request, order_id):

    try:
        order = Order.objects.select_related('delivery_person').get(order_id=order_id)
        return JsonResponse({
            'success': True,
            'order_id': order.order_id,
            'status': order.status,
            'total_amount': str(order.total_amount),
            'delivery_person': order.delivery_person.name if order.delivery_person else None
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Order not found'
        }, status=404)
