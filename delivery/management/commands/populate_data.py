"""
Management command to populate database with sample data
Place this file at: delivery/management/commands/populate_data.py

Run: python manage.py populate_data
"""

from django.core.management.base import BaseCommand
from delivery.models import Customer, Restaurant, MenuItem, DeliveryPersonnel, Order, OrderItem
from decimal import Decimal
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        self.stdout.write('Clearing existing data...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
        Restaurant.objects.all().delete()
        Customer.objects.all().delete()
        DeliveryPersonnel.objects.all().delete()
        
        self.stdout.write('Creating customers...')
        customers = [
            Customer.objects.create(
                name='Rajesh Kumar',
                email='rajesh@gmail.com',
                phone='9841234567',
                address='Thamel, Kathmandu'
            ),
            Customer.objects.create(
                name='Sita Sharma',
                email='sita.sharma@gmail.com',
                phone='9851234568',
                address='Lazimpat, Kathmandu'
            ),
            Customer.objects.create(
                name='Amit Thapa',
                email='amit.thapa@yahoo.com',
                phone='9861234569',
                address='Durbarmarg, Kathmandu'
            ),
            Customer.objects.create(
                name='Priya Rana',
                email='priya.rana@gmail.com',
                phone='9871234570',
                address='Baneshwor, Kathmandu'
            ),
            Customer.objects.create(
                name='Kiran Shrestha',
                email='kiran.shrestha@hotmail.com',
                phone='9881234571',
                address='Pulchowk, Lalitpur'
            ),
            Customer.objects.create(
                name='Anita Gurung',
                email='anita.gurung@gmail.com',
                phone='9891234572',
                address='Koteshwor, Kathmandu'
            ),
            Customer.objects.create(
                name='Bikash Tamang',
                email='bikash.tamang@gmail.com',
                phone='9801234573',
                address='Maharajgunj, Kathmandu'
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {len(customers)} customers'))
        
        self.stdout.write('Creating restaurants...')
        restaurants = [
            Restaurant.objects.create(
                name='Spice Garden',
                address='Thamel, Kathmandu',
                phone='014123456',
                rating=Decimal('4.5'),
                cuisine_type='Indian'
            ),
            Restaurant.objects.create(
                name='Dragon Wok',
                address='Durbar Marg, Kathmandu',
                phone='014123457',
                rating=Decimal('4.2'),
                cuisine_type='Chinese'
            ),
            Restaurant.objects.create(
                name='Pizza Paradise',
                address='Jhamsikhel, Lalitpur',
                phone='015123458',
                rating=Decimal('4.7'),
                cuisine_type='Italian'
            ),
            Restaurant.objects.create(
                name='Burger Junction',
                address='New Road, Kathmandu',
                phone='014123459',
                rating=Decimal('4.0'),
                cuisine_type='Fast Food'
            ),
            Restaurant.objects.create(
                name='Taco House',
                address='Kupondole, Lalitpur',
                phone='015123460',
                rating=Decimal('4.3'),
                cuisine_type='Mexican'
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {len(restaurants)} restaurants'))
        
        self.stdout.write('Creating menu items...')
        
        spice_items = [
            MenuItem.objects.create(
                restaurant=restaurants[0],
                name='Butter Chicken',
                description='Creamy tomato-based chicken curry',
                price=Decimal('450.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[0],
                name='Paneer Tikka',
                description='Grilled cottage cheese with spices',
                price=Decimal('350.00'),
                category='Starter',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[0],
                name='Naan',
                description='Traditional Indian bread',
                price=Decimal('80.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[0],
                name='Gulab Jamun',
                description='Sweet milk-solid dumplings',
                price=Decimal('120.00'),
                category='Dessert',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[0],
                name='Mango Lassi',
                description='Sweet mango yogurt drink',
                price=Decimal('150.00'),
                category='Beverage',
                is_available=True
            ),
        ]
        
        dragon_items = [
            MenuItem.objects.create(
                restaurant=restaurants[1],
                name='Fried Rice',
                description='Stir-fried rice with vegetables',
                price=Decimal('280.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[1],
                name='Chicken Chow Mein',
                description='Stir-fried noodles with chicken',
                price=Decimal('320.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[1],
                name='Spring Rolls',
                description='Crispy vegetable rolls',
                price=Decimal('200.00'),
                category='Starter',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[1],
                name='Manchurian',
                description='Spicy vegetable balls',
                price=Decimal('250.00'),
                category='Starter',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[1],
                name='Hot and Sour Soup',
                description='Spicy and tangy soup',
                price=Decimal('180.00'),
                category='Starter',
                is_available=True
            ),
        ]
        
        pizza_items = [
            MenuItem.objects.create(
                restaurant=restaurants[2],
                name='Margherita Pizza',
                description='Classic tomato and mozzarella pizza',
                price=Decimal('600.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[2],
                name='Pepperoni Pizza',
                description='Pizza topped with pepperoni',
                price=Decimal('750.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[2],
                name='Garlic Bread',
                description='Toasted bread with garlic butter',
                price=Decimal('180.00'),
                category='Starter',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[2],
                name='Pasta Carbonara',
                description='Creamy pasta with bacon',
                price=Decimal('480.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[2],
                name='Tiramisu',
                description='Italian coffee-flavored dessert',
                price=Decimal('280.00'),
                category='Dessert',
                is_available=True
            ),
        ]
        
        burger_items = [
            MenuItem.objects.create(
                restaurant=restaurants[3],
                name='Classic Burger',
                description='Beef patty with lettuce and tomato',
                price=Decimal('350.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[3],
                name='Chicken Burger',
                description='Grilled chicken breast burger',
                price=Decimal('380.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[3],
                name='French Fries',
                description='Crispy golden fries',
                price=Decimal('150.00'),
                category='Snack',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[3],
                name='Chicken Wings',
                description='Spicy fried chicken wings',
                price=Decimal('280.00'),
                category='Starter',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[3],
                name='Chocolate Shake',
                description='Thick chocolate milkshake',
                price=Decimal('220.00'),
                category='Beverage',
                is_available=True
            ),
        ]
        
        taco_items = [
            MenuItem.objects.create(
                restaurant=restaurants[4],
                name='Chicken Tacos',
                description='Soft tacos with grilled chicken',
                price=Decimal('420.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[4],
                name='Beef Burrito',
                description='Wrapped tortilla with beef filling',
                price=Decimal('480.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[4],
                name='Nachos',
                description='Tortilla chips with cheese',
                price=Decimal('280.00'),
                category='Snack',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[4],
                name='Quesadilla',
                description='Cheese-filled tortilla',
                price=Decimal('350.00'),
                category='Main Course',
                is_available=True
            ),
            MenuItem.objects.create(
                restaurant=restaurants[4],
                name='Churros',
                description='Fried dough pastry with sugar',
                price=Decimal('180.00'),
                category='Dessert',
                is_available=True
            ),
        ]
        
        all_items = spice_items + dragon_items + pizza_items + burger_items + taco_items
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_items)} menu items'))
        
        self.stdout.write('Creating delivery personnel...')
        delivery_people = [
            DeliveryPersonnel.objects.create(
                name='Ram Bahadur',
                phone='9841111111',
                vehicle_type='Bike',
                is_available=True
            ),
            DeliveryPersonnel.objects.create(
                name='Shyam Karki',
                phone='9851111112',
                vehicle_type='Scooter',
                is_available=True
            ),
            DeliveryPersonnel.objects.create(
                name='Hari Prasad',
                phone='9861111113',
                vehicle_type='Bike',
                is_available=False
            ),
            DeliveryPersonnel.objects.create(
                name='Krishna Lama',
                phone='9871111114',
                vehicle_type='Bicycle',
                is_available=True
            ),
            DeliveryPersonnel.objects.create(
                name='Gopal Rai',
                phone='9881111115',
                vehicle_type='Car',
                is_available=True
            ),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {len(delivery_people)} delivery personnel'))
        
        self.stdout.write('Creating orders...')
        
        statuses = ['Pending', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered']
        
        order1 = Order.objects.create(
            customer=customers[0],
            restaurant=restaurants[0],
            delivery_person=delivery_people[0],
            total_amount=Decimal('680.00'),
            status='Delivered',
            delivery_address=customers[0].address
        )
        OrderItem.objects.create(order=order1, menu_item=spice_items[0], quantity=1, item_price=spice_items[0].price)
        OrderItem.objects.create(order=order1, menu_item=spice_items[2], quantity=2, item_price=spice_items[2].price)
        OrderItem.objects.create(order=order1, menu_item=spice_items[4], quantity=1, item_price=spice_items[4].price)
        
        order2 = Order.objects.create(
            customer=customers[1],
            restaurant=restaurants[2],
            delivery_person=delivery_people[1],
            total_amount=Decimal('1060.00'),
            status='Out for Delivery',
            delivery_address=customers[1].address
        )
        OrderItem.objects.create(order=order2, menu_item=pizza_items[1], quantity=1, item_price=pizza_items[1].price)
        OrderItem.objects.create(order=order2, menu_item=pizza_items[2], quantity=1, item_price=pizza_items[2].price)
        OrderItem.objects.create(order=order2, menu_item=pizza_items[4], quantity=1, item_price=pizza_items[4].price)
        
        order3 = Order.objects.create(
            customer=customers[2],
            restaurant=restaurants[1],
            delivery_person=delivery_people[3],
            total_amount=Decimal('800.00'),
            status='Preparing',
            delivery_address=customers[2].address
        )
        OrderItem.objects.create(order=order3, menu_item=dragon_items[1], quantity=2, item_price=dragon_items[1].price)
        OrderItem.objects.create(order=order3, menu_item=dragon_items[2], quantity=1, item_price=dragon_items[2].price)
        OrderItem.objects.create(order=order3, menu_item=dragon_items[4], quantity=1, item_price=dragon_items[4].price)
        
        order4 = Order.objects.create(
            customer=customers[3],
            restaurant=restaurants[3],
            delivery_person=delivery_people[4],
            total_amount=Decimal('880.00'),
            status='Confirmed',
            delivery_address=customers[3].address
        )
        OrderItem.objects.create(order=order4, menu_item=burger_items[0], quantity=1, item_price=burger_items[0].price)
        OrderItem.objects.create(order=order4, menu_item=burger_items[1], quantity=1, item_price=burger_items[1].price)
        OrderItem.objects.create(order=order4, menu_item=burger_items[2], quantity=1, item_price=burger_items[2].price)
        
        order5 = Order.objects.create(
            customer=customers[4],
            restaurant=restaurants[4],
            delivery_person=delivery_people[0],
            total_amount=Decimal('900.00'),
            status='Delivered',
            delivery_address=customers[4].address
        )
        OrderItem.objects.create(order=order5, menu_item=taco_items[0], quantity=1, item_price=taco_items[0].price)
        OrderItem.objects.create(order=order5, menu_item=taco_items[1], quantity=1, item_price=taco_items[1].price)
        
        order6 = Order.objects.create(
            customer=customers[5],
            restaurant=restaurants[0],
            delivery_person=delivery_people[1],
            total_amount=Decimal('970.00'),
            status='Out for Delivery',
            delivery_address=customers[5].address
        )
        OrderItem.objects.create(order=order6, menu_item=spice_items[0], quantity=2, item_price=spice_items[0].price)
        OrderItem.objects.create(order=order6, menu_item=spice_items[3], quantity=1, item_price=spice_items[3].price)
        
        order7 = Order.objects.create(
            customer=customers[6],
            restaurant=restaurants[2],
            delivery_person=delivery_people[3],
            total_amount=Decimal('1080.00'),
            status='Pending',
            delivery_address=customers[6].address
        )
        OrderItem.objects.create(order=order7, menu_item=pizza_items[0], quantity=1, item_price=pizza_items[0].price)
        OrderItem.objects.create(order=order7, menu_item=pizza_items[3], quantity=1, item_price=pizza_items[3].price)
        
        order8 = Order.objects.create(
            customer=customers[0],
            restaurant=restaurants[3],
            delivery_person=delivery_people[4],
            total_amount=Decimal('650.00'),
            status='Delivered',
            delivery_address=customers[0].address
        )
        OrderItem.objects.create(order=order8, menu_item=burger_items[1], quantity=1, item_price=burger_items[1].price)
        OrderItem.objects.create(order=order8, menu_item=burger_items[3], quantity=1, item_price=burger_items[3].price)
        
        self.stdout.write(self.style.SUCCESS('Created 8 orders with order items'))
        
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('DATABASE POPULATED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Customers: {Customer.objects.count()}')
        self.stdout.write(f'Restaurants: {Restaurant.objects.count()}')
        self.stdout.write(f'Menu Items: {MenuItem.objects.count()}')
        self.stdout.write(f'Delivery Personnel: {DeliveryPersonnel.objects.count()}')
        self.stdout.write(f'Orders: {Order.objects.count()}')
        self.stdout.write(f'Order Items: {OrderItem.objects.count()}')