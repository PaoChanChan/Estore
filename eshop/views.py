from django.http import HttpResponse
from django.shortcuts import render
from tienda.models import Producto

# Create your views here.

def home(request):
    
    productos = Producto.objects.all().filter(disponibilidad=True)
    
    context = {
        'productos': productos,
    }   
    return render(request, 'home.html', context)