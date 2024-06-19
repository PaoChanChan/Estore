from django.http import HttpResponse
from django.shortcuts import render
from tienda.models import Producto, Opiniones

# Create your views here.

def home(request):
    
    productos = Producto.objects.all().filter(disponibilidad=True).order_by('-fecha_creacion')
    
    # Mostrando las opiniones en la homepage
    for producto in productos:
        opiniones = Opiniones.objects.filter(producto_id=producto.id, estado=True)
    
    context = {
        'productos': productos,
        'opiniones' : opiniones,
    }   
    return render(request, 'home.html', context)