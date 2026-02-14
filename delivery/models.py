from django.db import models
from django.core.validators import MinValueValidator ,MaxValueValidator
from decimal import Decimal
# Create your models here.



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customer'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
    


class Restaurant(models.Model):
    CUISINE_CHOICES = [
        ('Indian' , 'Indian'),
        ('Chinese', 'Chinese'),
        ('Italian', 'Italian'),
        ('Mexican', 'Mexican'),
        ('Fast Food', 'Fast Food'),
        ('Continental', 'Continental'),
    ]

    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0),MaxValueValidator(5.0)]
    )

    cuisine_type = models.CharField(max_length=50,choices=CUISINE_CHOICES)

    class Meta:
        db_table = 'restaurant'
        ordering = ['-rating']

    def __str__(self):
        return f"{self.name} - {self.cuisine_type}"
    


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Stater','Stater'),
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Beverage', 'Beverage'),
        ('Snack', 'Snack'),
    ]

    item_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name='menu_items'
        )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_available = models.BooleanField(default=True)


    class Meta:
        db_table = 'menu_item'
        ordering = ['category','name']

    def __str__(self):
        return f"{self.name} - Rs.{self.price} ({self.restaurant.name})"


class DeliveryPersonnel(models.Model):
    VEHICLE_CHOICES = [
        ('Bike', 'Bike'),
        ('Scooter', 'Scooter'),
        ('Car', 'Car'),
        ('Bicycle', 'Bicycle'),
    ]
    
    delivery_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES)
    is_available = models.BooleanField(default=True)


    class Meta:
        db_table = 'delivery_personnel'
        verbose_name_plural = 'Delivery Personnel'
    
    def __str__(self):
        status = "Available" if self.is_available else "Busy"
        return f"{self.name} - {self.vehicle_type} ({status})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'                     
        )
    
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE,
        related_name='orders'
    )

    delivery_person = models.ForeignKey(
        DeliveryPersonnel, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )

    delivery_address = models.TextField()

    class Meta:
        db_table = 'order_table'
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.customer.name} - Rs.{self.total_amount}"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    menu_item = models.ForeignKey(
        MenuItem, 
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    item_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
            db_table = 'order_item'
        
    def get_subtotal(self):
        return self.quantity * self.item_price
        
    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity} (Order #{self.order.order_id})"
        
    def save(self, *args, **kwargs):
        if not self.item_price:
            self.item_price = self.menu_item.price
        super().save(*args, **kwargs)
