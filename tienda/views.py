from django.shortcuts import render, get_object_or_404
from .models import Producto
from categoria.models import Categoria
from carts.models import CartItem
from django.db.models import Q
from django.db.models.functions import Lower
from unidecode import unidecode
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

def tienda(request, categoria_slug=None):
    """Función que muestra todos los artículos en "escaparate" y los distribuye por páginas"""
    categorias = None
    productos = None
    
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, disponibilidad=True)
        paginator = Paginator(productos, 3) # Paginación y artículos mostrados por página
        page = request.GET.get('page')
        paged_productos = paginator.get_page(page)
        numero_productos = productos.count()
    
    else:
        productos = Producto.objects.all().filter(disponibilidad=True).order_by('id')
        paginator = Paginator(productos, 6)
        page = request.GET.get('page')
        paged_productos = paginator.get_page(page)
        numero_productos = productos.count()
    
     # Imprimir el número de productos obtenidos en la consola del servidor
    print("Número de productos:", len(productos))
    
    context = {
        'productos': paged_productos,
        'numero_productos' : numero_productos
    }   
    
    return render(request, 'tienda/tienda.html', context)


def detalle_producto(request, categoria_slug, producto_slug):
    """Función que devuelve la información de un producto"""
    
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



def search(request):
    """Función de motor de búsqueda"""
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        if keyword:
            productos = Producto.objects.order_by('-fecha_creacion').filter(
            Q(nombre_producto__icontains=unidecode(keyword)) | 
            Q(descripcion_producto__icontains=unidecode(keyword)))
            numero_productos = productos.count()

        
            
    context = {
        'productos': productos,
        'numero_productos' : numero_productos,

    }
    return render(request, 'tienda/tienda.html', context)