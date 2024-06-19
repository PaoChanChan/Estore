from django.db import models
from categoria.models import Categoria
from cuentas.models import Cuenta
from django.urls import reverse
from django.conf import settings
from django.db.models import Avg, Count


# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion_producto = models.TextField(max_length=500, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='imagenes/productos')
    stock_maximo = models.IntegerField(default=0)
    stock_disponible = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='productos', default=2)  # Aquí '1' es el ID del usuario predeterminado

    # vendedor = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    
    def get_url(self):
        return reverse('detalle_producto', args=[self.categoria.slug, self.slug])
    
    def opiniones_media(self):
        opiniones = Opiniones.objects.filter(producto=self, estado=True).aggregate(media=Avg('puntuacion'))
        avg = 0
        if opiniones['media'] is not None:
            avg=float(opiniones['media'])
            return avg
    
    def opiniones_count(self):
        opiniones = Opiniones.objects.filter(producto=self, estado=True).aggregate(count=Count('id'))
        count = 0
        if opiniones['count'] is not None:
            count=int(opiniones['count'])
            return count

    
    def __str__(self):
        return self.nombre_producto
    

class VariationManager(models.Manager):
    def colores(self):
        return super(VariationManager, self).filter(variacion_categoria='color', is_active=True)
    
    def marca(self):
        return super(VariationManager,self).filter(variacion_categoria='color', is_active=True)
    

variacion_categoria_eleccion = (
    ('color', 'color'),
    ('marca', 'marca'),
)    
    
class Variaciones(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variacion_categoria = models.CharField(max_length=100, choices=variacion_categoria_eleccion)
    valor_variacion = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.valor_variacion
    
class Opiniones(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100, blank=True)
    opinion = models.TextField(max_length=500, blank=True)
    puntuacion = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    estado = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asunto


class GaleriaProducto(models.Model):
    producto = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='tienda/productos', max_length=255)

    def __str__(self):
        return self.product.nombre_producto

    class Meta:
        verbose_name = 'galeriaproducto'
        verbose_name_plural = 'galeria producto'