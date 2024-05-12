from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto
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
    producto = Producto.objects.get(id=id_producto) # Coger el producto
   
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Hace que el carrito coja la id (key) en el momento.
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        
    cart.save()    
    
    try:
        cart_item = CartItem.objects.get(producto=producto, cart=cart)
        cart_item.cantidad += 1    # Incrementa los productos en el carro
        cart_item.save()
    
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(producto=producto, cantidad=1, cart=cart)
        cart_item.save()
    
    return redirect('cart')

def remove_cart(request, id_producto):
    """Función para eliminar items del carrito"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    producto = get_object_or_404(Producto, id=id_producto)
    cart_item = CartItem.objects.get(producto=producto, cart=cart)
    
    if cart_item.cantidad > 1:
        cart_item.cantidad -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, id_producto):
    """Función para eliminar items del carrito"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    producto = get_object_or_404(Producto, id=id_producto)
    cart_item = CartItem.objects.get(producto=producto, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, cantidad=0, cart_items=None):
    try:
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