from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Variaciones, GaleriaProducto, Opiniones
from categoria.models import Categoria
from carts.models import CartItem
from django.db.models import Q
from django.db.models.functions import Lower

from unidecode import unidecode
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import OpinionesForm
from django.contrib import messages
from pedidos.models import ProductoPedido

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
    
     
    #print("Número de productos:", len(productos))
    
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
    
    # Con esto confirmamos que el producto ha sido adquirido por el usuario para permitirle hacer una reseña:
    if request.user.is_authenticated:
        try:
            producto_pedido = ProductoPedido.objects.filter(usuario=request.user, producto_id=producto_unico.id).exists()
        except ProductoPedido.DoesNotExist:
            producto_pedido = None
    else:
        producto_pedido = None

    # Mostrar opiniones:
    opiniones = Opiniones.objects.filter(producto_id=producto_unico.id, estado=True)

    # Galeria:
    galeria_producto = GaleriaProducto.objects.filter(producto_id=producto_unico.id)
    
    # Variaciones:
    colores = Variaciones.objects.filter(producto=producto_unico, variacion_categoria='color', is_active=True)
    marcas = Variaciones.objects.filter(producto=producto_unico, variacion_categoria='marca', is_active=True)

    context = {
        'producto_unico': producto_unico,
        'in_cart'       : in_cart,
        'producto_pedido': producto_pedido,
        'opiniones': opiniones,
        'galeria_producto': galeria_producto,
        'colores': colores,
        'marcas': marcas,
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

def publicar_opinion(request, producto_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            opiniones = Opiniones.objects.get(usuario__id=request.user.id, producto__id=producto_id)
            form = Opiniones(request.POST, instance=opiniones)
            form.save()
            messages.success(request, 'Se ha modificado tu comentario.')
            return redirect(url)
        except Opiniones.DoesNotExist:
            form = OpinionesForm(request.POST)
            if form.is_valid():
                data = Opiniones()
                data.asunto = form.cleaned_data['asunto']
                data.puntuacion = form.cleaned_data['puntuacion']
                data.opinion = form.cleaned_data['opinion']
                data.ip = request.META.get('REMOTE_ADDR')
                data.producto_id = producto_id
                data.usuario_id= request.user.id
                data.save()
                messages.success(request, '¡Gracias! Nos importa mucho tu opinión.')
                return redirect(url)