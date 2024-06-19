from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForm, UsuarioForm, PerfilUsuarioForm
from .models import Cuenta, PerfilUsuario
from pedidos.models import Pedido, ProductoPedido
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from tienda.models import Producto

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Create your views here.

def registrarse(request):
    """Función para crear una cuenta"""
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            telefono = form.cleaned_data['telefono']
            
            usuario = Cuenta.objects.create_user(nombre=nombre,
                                                  apellido=apellido,
                                                  username=username,
                                                  email=email,
                                                  password=password,
                                                  telefono=telefono)
            usuario.is_active = True
            usuario.save()
            messages.success(request, 'Cuenta creada con éxito.')

            
            print(usuario.nombre)
            
            #  CREACIÓN DE PERFIL DE USUARIO
            perfil = PerfilUsuario(usuario=usuario, direccion_1='', direccion_2='',
                                    ciudad='', municipio='', pais='')
            perfil.id_usuario = usuario.id
            perfil.save()
            messages.success(request, 'Perfil creado con éxito.')
            
             # Iniciar sesión automáticamente
            usuario = auth.authenticate(email=email, password=password)
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, 'Registrado y conectado con éxito.')
                return redirect('dashboard')
            

    else:
        form = RegistroForm()
    
    context = {
        'form': form,
    }
    return render(request, 'cuentas/registrarse.html', context)

@csrf_protect
def login(request):
    """Función para acceder a la cuenta"""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        usuario = auth.authenticate(email=email, password=password)
        
        if usuario is not None:
            auth.login(request, usuario)
            if usuario.is_seller:
                return redirect('seller_dashboard')
            else:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        
                        # Extraer variaciones de los productos por el id del carrito                   
                        variacion_productos = []
                        for item in cart_item:
                            variacion = item.variaciones.all()
                            variacion_productos.append(list(variacion))               

                        # Extraer los items del carrito del usuario para acceder a las variaciones de sus productos
                        cart_item = CartItem.objects.filter(usuario=usuario)
                        lista_variaciones = []
                        lista_id = []
                        for item in cart_item:
                            variacion = item.variaciones.all()
                            lista_variaciones.append(list(variacion))
                            lista_id.append(item.id)
                        
                        for pr in variacion_productos:
                            if pr in lista_variaciones:
                                index = lista_variaciones.index(pr)
                                item_id = lista_id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.cantidad += 1
                                item.usuario = usuario
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.usuario = usuario
                                    item.save()
                except Cart.DoesNotExist:
                    pass
                
                messages.success(request, 'Estás conectado/a.')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('dashboard')
        
        else:
            messages.error(request, 'Credenciales erróneas. Inténtalo de nuevo.')
            return redirect('login')
    return render(request, 'cuentas/login.html')


@login_required(login_url = 'login')   # Solo podemos salir si estamos dentro.
def logout(request): 
    """Función para cerrar sesión"""
    
    auth.logout(request)
    messages.success(request, '¡Hasta pronto!')
    return redirect('login')
    

@login_required(login_url = 'login')  
def dashboard(request):
    """Función para mostrar el dashboard del cliente."""
    
    pedidos = Pedido.objects.order_by('-fecha').filter(usuario=request.user.id, confirmado=True)
    cantidad_pedidos = pedidos.count()
    
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user.id)
    
    context = {
        'cantidad_pedidos' : cantidad_pedidos,
        'perfil_usuario' : perfil_usuario,
    }
    return render(request, 'cuentas/dashboard.html', context)
 
    
@login_required(login_url='login')
def mis_pedidos(request):   
    """Función para mostrar todos los pedidos del usuario cliente"""
    
    pedidos = Pedido.objects.filter(usuario=request.user, confirmado=True).order_by('-fecha')
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'cuentas/mis_pedidos.html', context)



@login_required(login_url = 'login')  
def seller_dashboard(request):
    """Función para mostrar el dashboard del vendedor y la gráfica de ventas."""
    
        # Extraer los datos de la base de datos
    producto_pedidos = ProductoPedido.objects.all()
    
    # Crear un DataFrame de pandas
    data = {
        'producto': [],
        'cantidad': [],
        'precio_producto': [],
        'fecha': [],
    }
    
    for pedido in producto_pedidos:
        data['producto'].append(pedido.producto.nombre_producto)
        data['cantidad'].append(pedido.cantidad)
        data['precio_producto'].append(pedido.precio_producto)
        data['fecha'].append(pedido.fecha)

    df = pd.DataFrame(data)
    
    # Convertir la columna de fecha en formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Agrupar por mes y producto para obtener las ventas
    df['mes'] = df['fecha'].dt.to_period('M').astype(str)
    ventas_mensuales = df.groupby(['mes', 'producto']).agg({'cantidad': 'sum', 'precio_producto': 'sum'}).reset_index()

    # Calcular los beneficios (asumiendo precio_producto como el beneficio unitario)
    ventas_mensuales['beneficio'] = ventas_mensuales['cantidad'] * ventas_mensuales['precio_producto']
    
    # Crear los gráficos de ventas y beneficios usando Plotly
    fig_ventas = px.bar(ventas_mensuales, x='mes', y='cantidad', color='producto', title='Ventas Mensuales (Cantidad de Productos Vendidos)')
    fig_beneficios = px.bar(ventas_mensuales, x='mes', y='beneficio', color='producto', title='Beneficios Mensuales')
    
    # Convertir las figuras a HTML
    grafico_ventas = pio.to_html(fig_ventas, full_html=False)
    grafico_beneficios = pio.to_html(fig_beneficios, full_html=False)
    
    context = {
        'grafico_ventas': grafico_ventas,
        'grafico_beneficios': grafico_beneficios,
    }
    
    return render(request, 'cuentas/seller_dashboard.html', context)

@login_required(login_url = 'login')  
def seller_productos(request):
    """Función para mostrar el listado de productos y stock del vendedor."""
    
    productos_vendedor = Producto.objects.filter(vendedor=request.user).order_by('-stock_disponible')
    stock_al_90 = None 
    
    for producto in productos_vendedor:
        stock_al_90 = 0.9 * producto.stock_maximo
    
    context = {
        'productos_vendedor': productos_vendedor,
        'stock_al_90' : stock_al_90,
    }
    
    return render(request, 'cuentas/seller_productos.html', context)
    
@login_required(login_url='login')
def editar_perfil(request): 
    """Función de edición de perfil"""
    
    perfil_usuario = get_object_or_404(PerfilUsuario, usuario=request.user)
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, 'Se ha actualizado tu perfil.')
            return redirect('editar_perfil')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil_usuario)
    context = {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'perfil_usuario': perfil_usuario,
    }
    return render(request, 'cuentas/editar_perfil.html', context)


@login_required(login_url='login')
def cambiar_password(request):    
    """Función para cambiar contraseña"""
    
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        usuario = Cuenta.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = usuario.check_password(current_password)
            if success:
                usuario.set_password(new_password)
                usuario.save()
                # auth.logout(request)
                messages.success(request, 'Contraseña modificada con éxito.')
                return redirect('cambiar_password')
            else:
                messages.error(request, 'Por favor, ingresa la contraseña actual.')
                return redirect('cambiar_password')
        else:
            messages.error(request, 'La contraseña no coincide.')
            return redirect('cambiar_password')
    return render(request, 'cuentas/cambiar_password.html')


@login_required(login_url='login')
def detalle_pedido(request, id_pedido):  
    """Función para mostrar los detalles de un pedido en concreto"""
    
    detalle_pedido = ProductoPedido.objects.filter(pedido__numero_pedido=id_pedido)
    pedido = Pedido.objects.get(numero_pedido=id_pedido)
    total = 0
    for i in detalle_pedido:
        total += i.precio_producto * i.cantidad

    context = {
        'detalle_pedido': detalle_pedido,
        'pedido': pedido,
        'total': total,
    }
    return render(request, 'cuentas/detalle_pedido.html', context)

