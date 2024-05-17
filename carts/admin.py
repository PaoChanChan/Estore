from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'fecha_creacion']
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cart', 'cantidad', 'activo']
    
    
    
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)