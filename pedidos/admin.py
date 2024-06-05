from django.contrib import admin
from .models import Pago, Pedido, ProductoPedido
# Register your models here.


class ProductoPedidoInline(admin.TabularInline):
    model = ProductoPedido
    readonly_fields = ('pago', 'usuario', 'producto', 'cantidad', 'precio_producto', 'confirmado')
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'full_name', 'telefono', 'email', 'ciudad', 'precio_total_pedido', 'iva', 'estado', 'confirmado', 'fecha']
    list_filter = ['estado', 'confirmado']
    search_fields = ['numero_pedido', 'nombre', 'apellido', 'telefono', 'email']
    list_per_page = 20
    inlines = [ProductoPedidoInline]

admin.site.register(Pago)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ProductoPedido)