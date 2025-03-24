from django.contrib import admin
from .models import Category, Product, WishlistItem, CartItem, Order, ProductImage


admin.site.register(Category)
admin.site.register(WishlistItem)
admin.site.register(CartItem)
admin.site.register(Order)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    can_delete = True  
    fields = ['image'] 


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]



try:
    admin.site.unregister(Product)
except admin.sites.NotRegistered:
    pass

admin.site.register(Product, ProductAdmin)
