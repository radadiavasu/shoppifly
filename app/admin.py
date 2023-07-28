from django.contrib import admin
from app.models import *

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name',
                    'locality', 'city', 'zipcode', 'state']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price',
                    'discounted_price', 'description', 'brand', 'category', 'product_image']
    
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']    
    


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['shoe_sizes', 'topwear_sizes', 'bottomwear_sizes']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product',
                    'quantity']


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'product', 'quantity', 'ordered_date', 'status']
    
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'phone_number', 'email', 'subject', 'message']