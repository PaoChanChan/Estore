from .models import Cart, CartItem
from .views import _cart_id


def contador(request):
    
    cuenta_carrito = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(usuario=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            for cart_item in cart_items:
                cuenta_carrito += cart_item.cantidad
        
        except Cart.DoesNotExist:
            cuenta_carrito = 0
    
    return dict(cuenta_carrito=cuenta_carrito)
                