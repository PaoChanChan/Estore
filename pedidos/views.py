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


def pago(request):
#     """Función para gestionar el pago. Incompleta pero abierta para mejoras futuras del proyecto."""

#     body = json.loads(request.body)
#     pedido = Pedido.objects.get(usuario=request.user, confirmado=True, numero_pedido=body['pedidoID'])
#     # Volcar productos al pedido
#     cart_items = CartItem.objects.filter(usuario=request.user)
   

#     for item in cart_items:
#         productopedido = ProductoPedido()
#         productopedido.id_pedido = pedido.id
#         productopedido.pago = pago
#         productopedido.id_usuario = request.user.id
#         productopedido.id_producto = item.id_producto
#         productopedido.cantidad = item.cantidad
#         productopedido.precio_producto = item.precio_producto
#         productopedido.confirmado = True
#         productopedido.save()

#         cart_item = CartItem.objects.get(id=item.id)
#         variacion_producto = cart_item.variaciones.all()
#         productopedido = ProductoPedido.objects.get(id=productopedido.id)
#         productopedido.variaciones.set(variacion_producto)
#         productopedido.save()


#         # Reducir cantidad de productos en el stock.
#         producto = Producto.objects.get(id=item.id_producto)
#         producto.stock -= item.cantidad
#         producto.save()

#     # Vaciar carrito
#     CartItem.objects.filter(usuario=request.user).delete()

    # # Email con información de pedido
    # asunto = '¡Gracias por tu pedido!'
    # message = render_to_string('pedidos/email_pedido_recibido.html', {
    #     'usuario': request.user,
    #     'pedido': pedido,
    # })
    # to_email = request.user.email
    # send_email = EmailMessage(asunto, message, to=[to_email])
    # send_email.send()

    # # Send order number and transaction id back to sendData method via JsonResponse
    # data = {
    #     'numero_pedido': pedido.numero_pedido,
    #     'transID': pago.id_pago,
    # }
    # return JsonResponse(data)
        return render(request, 'pedidos/pago.html')

def hacer_pedido(request, total=0, cantidad=0):
    usuario_actual = request.user

    # Si el carrito es igual o menor a 0, redirigimos a la tienda.
    cart_items = CartItem.objects.filter(usuario=usuario_actual)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('tienda')

    precio_final = 0
    iva = 0
    for cart_item in cart_items:
        total += (cart_item.producto.precio * cart_item.cantidad)
        cantidad += cart_item.cantidad
    iva = (21 * total) / 100
    precio_final = total + iva

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Almacenar los datos del pedido en la tabla Pedido
            pedido = Pedido()
            pedido.usuario = usuario_actual
            pedido.nombre = form.cleaned_data['nombre']
            pedido.apellido = form.cleaned_data['apellido']
            pedido.telefono = form.cleaned_data['telefono']
            pedido.email = form.cleaned_data['email']
            pedido.direccion_1 = form.cleaned_data['direccion_1']
            pedido.direccion_2 = form.cleaned_data['direccion_2']
            pedido.pais = form.cleaned_data['pais']
            pedido.municipio = form.cleaned_data['municipio']
            pedido.ciudad = form.cleaned_data['ciudad']
            pedido.nota_pedido = form.cleaned_data['nota_pedido']
            pedido.precio_total_pedido = precio_final
            pedido.iva = iva
            pedido.ip = request.META.get('REMOTE_ADDR')
            pedido.confirmado = True  # Aseguramos que el pedido se marca como confirmado
            pedido.save()

            # Generar número de pedido
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            fecha_actual = d.strftime("%Y%m%d")
            numero_pedido = fecha_actual + str(pedido.id)
            pedido.numero_pedido = numero_pedido
            pedido.save()

            # Volcar productos al pedido
            for item in cart_items:
                productopedido = ProductoPedido()
                productopedido.pedido = pedido
                productopedido.usuario = request.user
                productopedido.producto = item.producto
                productopedido.cantidad = item.cantidad
                productopedido.precio_producto = item.producto.precio
                productopedido.confirmado = True
                productopedido.save()

                variacion_producto = item.variaciones.all()
                productopedido.variaciones.set(variacion_producto)
                productopedido.save()

                # Reducir cantidad de productos en el stock.
                producto = Producto.objects.get(id=item.producto.id)
                producto.stock_disponible -= item.cantidad
                producto.save()

            # Vaciar carrito
            CartItem.objects.filter(usuario=request.user).delete()

            context = {
                'pedido': pedido,
                'cart_items': cart_items,
                'total': total,
                'iva': iva,
                'precio_final': precio_final,
            }
            return render(request, 'pedidos/pago.html', context)
        else:
            print(form.errors)
    else:
        return redirect('checkout')



# def pedido_completado(request):
#     numero_pedido = request.GET.get('numero_')
#     transID = request.GET.get('id_pago')

#     try:
#         pedido = Pedido.objects.get(numero_pedido=numero_pedido, confirmado=True)
#         productos_pedidos = ProductoPedido.objects.filter(id_pedido=pedido.id)

#         total = 0
#         for i in productos_pedidos:
#             total += i.precio_producto * i.cantidad

#         pago = Pago.objects.get(id_pago=transID)

#         context = {
#             'pedido': pedido,
#             'productos_pedidos': productos_pedidos,
#             'numero_pedido': pedido.numero_pedido,
#             'transID': pago.id_pago,
#             'pago': pago,
#             'total': total,
#         }
#         return render(request, 'pedidos/pedido_completado.html', context)
#     except (Pago.DoesNotExist, Pedido.DoesNotExist):
#         return redirect('home')