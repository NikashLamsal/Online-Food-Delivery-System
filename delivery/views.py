from django.shortcuts import render, get_object_or_404
from .models import Customer, Restaurant, MenuItem, Order, OrderItem, DeliveryPersonnel
from django.db.models import Count, Sum, Avg, Q

# Create your views here.
def home(request):

    context = {
        'total_customers': Customer.objects.count(),
        'total_restaurants': Restaurant.objects.count(),
        'total_orders': Order.objects.count(),
        'total_menu_items': MenuItem.objects.count(),
        'active_orders' : Order.objects.exclude(status__in = ['Delivered','Cancelled']),
        'recent_orders': Order.objects.select_related('customer', 'restaurant').order_by('-order_date')[:5],
    }
    
    return render(request,'delivery/home.html',context)

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

