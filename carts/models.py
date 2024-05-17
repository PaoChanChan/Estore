from django.db import models
from tienda.models import Producto, Variaciones

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variaciones, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=True)
    
    def sub_total(self):
        """Función que calcula el carrito"""
        return self.producto.precio * self.cantidad 
    
    def __unicode__(self):
        return self.producto.nombre