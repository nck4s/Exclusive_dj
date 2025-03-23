from django.contrib import admin
from .models import Category, Product, WishlistItem, CartItem, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(WishlistItem)
admin.site.register(CartItem)
admin.site.register(Order)
