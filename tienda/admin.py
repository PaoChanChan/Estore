from django.contrib import admin
from .models import Producto, Variaciones, Opiniones, GaleriaProducto
#import admin_thumbnails

# Register your models here.

#@admin_thumbnails.thumbnail('imagen')
class ProductGalleryInline(admin.TabularInline):
    modelo = GaleriaProducto
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'stock_disponible', 'stock_maximo', 'categoria', 'fecha_modificacion', 'disponibilidad')
    prepopulated_fields = {'slug' : ('nombre_producto',)}
    
class VariacionesAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variacion_categoria', 'valor_variacion', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('producto', 'variacion_categoria', 'valor_variacion')
    
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variaciones, VariacionesAdmin)
admin.site.register(Opiniones)
admin.site.register(GaleriaProducto)
