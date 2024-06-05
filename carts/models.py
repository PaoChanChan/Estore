from django.db import models
from tienda.models import Producto, Variaciones
from cuentas.models import Cuenta

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variaciones, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        """Función que calcula el carrito"""
        return self.producto.precio * self.cantidad 
    
    def __unicode__(self):
        return self.producto