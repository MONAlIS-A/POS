from django.contrib import admin
from . models import Product, Cart, Order, Profile

# product
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['id', 'title','selling_price','discounted_price','description','category','product_image']

# Cart
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','product','quantity']

# Order
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'product', 'order_quantity', 'date']

# Profile
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'address', 'phone', 'image']