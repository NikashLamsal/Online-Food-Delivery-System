from django.contrib import admin
from .models import Customer, Restaurant, MenuItem, DeliveryPersonnel, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('customer_id', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('customer_id', 'name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )



@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_id', 'name', 'cuisine_type', 'rating', 'phone')
    list_filter = ('cuisine_type', 'rating')
    search_fields = ('name', 'cuisine_type')
    readonly_fields = ('restaurant_id',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('restaurant_id', 'name', 'cuisine_type', 'rating')
        }),
        ('Contact Details', {
            'fields': ('phone', 'address')
        }),
    )



@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'restaurant', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available', 'restaurant')
    search_fields = ('name', 'description')
    readonly_fields = ('item_id',)
    list_editable = ('is_available',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_id', 'restaurant', 'name', 'category')
        }),
        ('Details', {
            'fields': ('description', 'price', 'is_available')
        }),
    )



@admin.register(DeliveryPersonnel)
class DeliveryPersonnelAdmin(admin.ModelAdmin):
    list_display = ('delivery_id', 'name', 'phone', 'vehicle_type', 'is_available')
    list_filter = ('vehicle_type', 'is_available')
    search_fields = ('name', 'phone')
    readonly_fields = ('delivery_id',)
    list_editable = ('is_available',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('delivery_id', 'name', 'phone')
        }),
        ('Work Details', {
            'fields': ('vehicle_type', 'is_available')
        }),
    )



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('order_item_id', 'get_subtotal')
    fields = ('order_item_id', 'menu_item', 'quantity', 'item_price', 'get_subtotal')
    
    def get_subtotal(self, obj):
        if obj.pk:
            return f"Rs.{obj.get_subtotal()}"
        return "Rs.0.00"
    get_subtotal.short_description = 'Subtotal'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'restaurant', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'order_date', 'restaurant')
    search_fields = ('customer__name', 'restaurant__name')
    readonly_fields = ('order_id', 'order_date')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'order_date', 'status')
        }),
        ('Customer & Restaurant', {
            'fields': ('customer', 'restaurant', 'delivery_person')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'total_amount')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Calculate total amount from order items
        super().save_model(request, obj, form, change)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'order', 'menu_item', 'quantity', 'item_price', 'get_subtotal_display')
    list_filter = ('order__order_date', 'menu_item__category')
    search_fields = ('order__order_id', 'menu_item__name')
    readonly_fields = ('order_item_id', 'get_subtotal_display')
    
    def get_subtotal_display(self, obj):
        return f"Rs.{obj.get_subtotal()}"
    get_subtotal_display.short_description = 'Subtotal'
    
    fieldsets = (
        ('Order Details', {
            'fields': ('order_item_id', 'order')
        }),
        ('Item Details', {
            'fields': ('menu_item', 'quantity', 'item_price', 'get_subtotal_display')
        }),
    )


admin.site.site_header = "Food Delivery System Admin"
admin.site.site_title = "Food Delivery Admin"
admin.site.index_title = "Welcome to Food Delivery Management"