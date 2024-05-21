from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto, Variaciones
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    """Función para extraer la clave de sesión de las cookies para el carrito."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, id_producto):
    """Función para agregar items al carrito"""
    # user_actual = request.user
    producto = Producto.objects.get(id=id_producto) # Coger el producto
    variacion_producto = []
    #  Si el usuario está registrado:
    #if request.user.is_authenticated:
        #variacion_producto = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variacion = Variaciones.objects.get(producto=producto, variacion_categoria__iexact=key, valor_variacion__iexact=value)
                variacion_producto.append(variacion)
                print(variacion)
            except:
                pass          
   
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Hace que el carrito coja la id (key) en el momento.
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        
    cart.save()    
    
    is_cart_item_exists = CartItem.objects.filter(producto=producto, cart=cart).exists()
    
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(producto=producto, cart=cart)
        lista_variaciones = []
        lista_id = []
        for item in cart_item:   #   Comprobamos si la variación seleccionada es parte de las existentes, y la agregamos a la lista
            variacion_existente = item.variaciones.all()
            lista_variaciones.append(list(variacion_existente))
            lista_id.append(item.id)
        print(lista_variaciones)    
        
        if variacion_producto in lista_variaciones:
            
            index = lista_variaciones.index(variacion_producto)
            item_id = lista_id[index]
            item = CartItem.objects.get(producto=producto, id=item_id)
            item.cantidad += 1
            item.save()
        
        else:
            
            item = CartItem.objects.create(producto=producto, cantidad=1, cart=cart)
            if len(variacion_producto) > 0:
                item.variaciones.clear()
                item.variaciones.add(*variacion_producto)
            item.save()
    
    else:
        cart_item = CartItem.objects.create(producto=producto, cantidad=1, cart=cart)
        if len(variacion_producto) > 0:
            cart_item.variaciones.clear()
            for item in variacion_producto:
                cart_item.variaciones.add(*variacion_producto)
        cart_item.save()
    
    return redirect('cart')

def remove_cart(request, id_producto, cart_item_id):
    """Función para eliminar carrito"""
    
    producto = get_object_or_404(Producto, id=id_producto)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    
    try:
        
        cart_item = CartItem.objects.get(producto=producto, cart=cart, id=cart_item_id)
        
        if cart_item.cantidad > 1:
            cart_item.cantidad -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, id_producto, cart_item_id):
    """Función para eliminar items del carrito"""
    
    producto = get_object_or_404(Producto, id=id_producto)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    
    cart_item = CartItem.objects.get(producto=producto, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, cantidad=0, cart_items=None):
    try:
        iva = 0
        precio_final = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,activo=True)
        
        for cart_item in cart_items:
            total += cart_item.sub_total()
            cantidad += cart_item.cantidad
        iva = (21 * total) / 100
        precio_final = total + iva
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'cantidad': cantidad,
        'cart_items': cart_items,
        'iva' : iva,
        'precio_final' : precio_final,
    }
    
    return render(request, 'tienda/cart.html', context) # Renderizar la plantilla del carrito con el contexto"""