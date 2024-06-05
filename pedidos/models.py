from django.db import models
from cuentas.models import Cuenta
from tienda.models import Producto, Variaciones



class Pago(models.Model):
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    id_pago = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=100)
    suma_pago = models.CharField(max_length=100) 
    estado = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_pago


class Pedido(models.Model):
    STATUS = (
        ('Nuevo', 'Nuevo'),
        ('Aceptado', 'Aceptado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    )

    usuario = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, blank=True, null=True)
    numero_pedido = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    direccion_1 = models.CharField(max_length=50)
    direccion_2 = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    nota_pedido = models.CharField(max_length=100, blank=True)
    precio_total_pedido = models.FloatField()
    iva = models.FloatField()
    estado = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    confirmado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.nombre} {self.apellido}'

    def full_address(self):
        return f'{self.direccion_1} {self.direccion_2}'

    def __str__(self):
        return self.nombre


class ProductoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, blank=True, null=True)
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variaciones, blank=True)
    cantidad = models.IntegerField()
    precio_producto = models.FloatField()
    confirmado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto.nombre_producto

"""class Ventas(models.Model):
    producto_pedido = models.ForeignKey(ProductoPedido, on_delete=models.CASCADE)"""
    