from django.contrib import admin
from .models import Producto

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'stock_disponible', 'stock_maximo', 'categoria', 'fecha_modificacion', 'disponibilidad')
    prepopulated_fields = {'slug' : ('nombre_producto',)}
    
    
admin.site.register(Producto, ProductoAdmin)
