from django.shortcuts import render, get_object_or_404
from .models import Producto
from categoria.models import Categoria
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
# Create your views here.

def tienda(request, categoria_slug=None):
    categorias = None
    productos = None
    
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, disponibilidad=True)
        numero_productos = productos.count()
    
    else:
        productos = Producto.objects.all().filter(disponibilidad=True)
        numero_productos = productos.count()
    
     # Imprimir el número de productos obtenidos en la consola del servidor
    print("Número de productos:", len(productos))
    
    context = {
        'productos': productos,
        'numero_productos' : numero_productos
    }   
    
    return render(request, 'tienda/tienda.html', context)


def detalle_producto(request, categoria_slug, producto_slug):
    
    try:
        producto_unico = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), producto=producto_unico).exists() # Si el item ya está en el carrito, True. Si no lo está, False.
        
    except Exception as e:
        raise e
    
    context = {
        'producto_unico': producto_unico,
        'in_cart' : in_cart,
    }
        
    return render(request, 'tienda/detalle_producto.html', context)
