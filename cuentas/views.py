from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Cuenta
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verificación email:
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def registrarse(request):
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            telefono = form.cleaned_data['telefono']
            password = form.cleaned_data['password']
            
            usuario = Cuenta.objects.create_user(nombre=nombre,
                                                  apellido=apellido,
                                                  username=username,
                                                  email=email,
                                                  telefono=telefono,
                                                  password=password)
            usuario.telefono = telefono
            usuario.save()
            
            #  EMAIL DE ACTIVACION DEL USUARIO
            current_site = get_current_site(request)
            mail_subject = 'Verificación de cuenta en CachaRock'
            message = render_to_string('cuentas/email_verificacion_cuenta.html', {
                'usuario': usuario,
                'dominio' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token' : default_token_generator.make_token(usuario),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Gracias por registrarte, te hemos enviado un email para verificar tu cuenta.')
            return redirect('/cuentas/login/?command=verificacion&email='+email)

    else:
        form = RegistroForm()
    
    context = {
        'form': form,
    }
    return render(request, 'cuentas/registrarse.html', context)


def login(request):
    """Función para acceder a la cuenta"""
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        usuario = auth.authenticate(email=email, password=password)
        
        if usuario is not None and usuario.is_active:
            auth.login(request, usuario)
            messages.success(request, 'Estás conectado/a.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales erróneas o cuenta no verificada. Inténtalo de nuevo.')
            return redirect('login')
        
    return render(request, 'cuentas/login.html')

@login_required(login_url = 'login')   # Solo podemos salir si estamos dentro.
def logout(request):
    
    auth.logout(request)
    messages.success(request, '¡Hasta pronto!')
    
    return redirect('login')

def activar(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        usuario = None  
    
    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        messages.success(request, 'Enhorabuena, tu cuenta ha sido activada.')
        return redirect('login')
    else:
        messages.error(request, 'Link de activación defectuoso')
        return redirect('registrarse')
    
@login_required(login_url = 'login')  
def dashboard(request):
    """Función para mostrar el dashboard de la cuenta."""
    
    return render(request, 'cuentas/dashboard.html')

def forgotPassword(request):
    """Función para recuperar contraseñas"""
    
    if request.method == 'POST':
        email = request.POST['email']
        if Cuenta.objects.filter(email=email).exists():
            usuario = Cuenta.objects.get(email__exact=email)
            #  EMAIL DE RESTAURACIÓN DE CONTRASEÑAS
            current_site = get_current_site(request)
            mail_subject = 'Restaurar contraseña'
            message = render_to_string('cuentas/email_restaurar_password.html', {
                'usuario': usuario,
                'dominio' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token' : default_token_generator.make_token(usuario),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Te hemos enviado un email para restaurar tu contraseña.')
            return redirect('login')
            
        else:
            messages.error(request,'La cuenta no existe')   
            return redirect('forgotPassword')
            
    return render(request, 'cuentas/forgotPassword.html')


def resetpassword_validar(request, uidb64, token):
    """Función para validar la neuva contraseña"""
      
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        usuario = None  
    
    if usuario is not None and default_token_generator.check_token(usuario, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor, introduce tu nueva contraseña')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Este enlace ha expirado.')
        return redirect('login')
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            usuario = Cuenta.objects.get(pk=uid)
            usuario.set_password(password)  #  Función necesaria de Django para que la base de datos recoja la nueva contraseña
            usuario.save()
            messages.success(request, 'Contraseña restaurada con éxito.')
            return redirect('login')
        
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('resetPassword')
    else:
           
        return render(request, 'cuentas/resetPassword.html')

