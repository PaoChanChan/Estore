from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import PedidoForm
import datetime
from .models import Pedido, Pago, ProductoPedido
import json
from tienda.models import Producto
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def pagos(request):
    body = json.loads(request.body)
    pedido = Pedido.objects.get(usuario=request.user, confirmado=False, numero_pedido=body['pedidoID'])

    # Transacciones
    pago = Pago(
        usuario = request.user,
        id_pago = body['transID'],
        metodo_pago = body['metodo_pago'],
        suma_pago = pedido.precio_total_pedido,
        estado = body['estado'],
    )
    pago.save()

    pedido.payment = pago
    pedido.confirmado = True
    pedido.save()

    # Volcar productos al pedido
    cart_items = CartItem.objects.filter(usuario=request.user)

    for item in cart_items:
        productopedido = ProductoPedido()
        productopedido.id_pedido = pedido.id
        productopedido.pago = pago
        productopedido.id_usuario = request.user.id
        productopedido.id_producto = item.id_producto
        productopedido.cantidad = item.cantidad
        productopedido.precio_producto = item.precio_producto
        productopedido.confirmado = True
        productopedido.save()

        cart_item = CartItem.objects.get(id=item.id)
        variacion_producto = cart_item.variaciones.all()
        productopedido = ProductoPedido.objects.get(id=productopedido.id)
        productopedido.variaciones.set(variacion_producto)
        productopedido.save()


        # Reducir cantidad de productos
        producto = Producto.objects.get(id=item.id_producto)
        producto.stock -= item.cantidad
        producto.save()

    # Vaciar carrito
    CartItem.objects.filter(usuario=request.user).delete()

    # Email con información de pedido
    asunto = '¡Gracias por tu pedido!'
    message = render_to_string('pedidos/email_pedido_recibido.html', {
        'usuario': request.user,
        'pedido': pedido,
    })
    to_email = request.user.email
    send_email = EmailMessage(asunto, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'numero_pedido': pedido.numero_pedido,
        'transID': pago.id_pago,
    }
    return JsonResponse(data)

def hacer_pedido(request, total=0, cantidad=0,):
    usuario_actual = request.user

    # Si el carrito es igual o menor a 0, redirigimos a la tienda.
    cart_items = CartItem.objects.filter(user=usuario_actual)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('tienda')

    precio_final = 0
    iva = 0
    for cart_item in cart_items:
        total += (cart_item.producto.precio * cart_item.cantidad)
        cantidad += cart_item.cantidad
    iva = (21 * total)/100
    precio_final = total + iva

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Almacenar los datos del pedido en la tabla
            data = Pedido()
            data.user = usuario_actual
            data.nombre = form.cleaned_data['nombre']
            data.apellido = form.cleaned_data['apellido']
            data.telefono = form.cleaned_data['telefono']
            data.email = form.cleaned_data['email']
            data.direccion_1_1 = form.cleaned_data['direccion_1']
            data.direccion_2 = form.cleaned_data['direccion_2']
            data.pais = form.cleaned_data['pais']
            data.municipio = form.cleaned_data['municipio']
            data.ciudad = form.cleaned_data['ciudad']
            data.nota_pedido = form.cleaned_data['nota_pedido']
            data.precio_total_pedido = precio_final
            data.iva = iva
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generar número de pedido
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            fecha_actual = d.strftime("%d%m%Y") 
            numero_pedido = fecha_actual + str(data.id)
            data.numero_pedido = numero_pedido
            data.save()

            pedido = Pedido.objects.get(user=usuario_actual, is_ordered=False, order_number=numero_pedido)
            context = {
                'pedido': pedido,
                'cart_items': cart_items,
                'total': total,
                'iva': iva,
                'precio_final': precio_final,
            }
            return render(request, 'pedidos/pagos.html', context)
    else:
        return redirect('checkout')


def pedido_completado(request):
    numero_pedido = request.GET.get('numero_')
    transID = request.GET.get('id_pago')

    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido, confirmado=True)
        productos_pedidos = ProductoPedido.objects.filter(id_pedido=pedido.id)

        total = 0
        for i in productos_pedidos:
            total += i.precio_producto * i.cantidad

        pago = Pago.objects.get(id_pago=transID)

        context = {
            'pedido': pedido,
            'productos_pedidos': productos_pedidos,
            'numero_pedido': pedido.numero_pedido,
            'transID': pago.id_pago,
            'pago': pago,
            'total': total,
        }
        return render(request, 'pedidos/pedido_completado.html', context)
    except (Pago.DoesNotExist, Pedido.DoesNotExist):
        return redirect('home')