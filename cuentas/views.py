from django.shortcuts import render
from .forms import RegistroForm
from .models import Cuenta

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
    else:
        form = RegistroForm()
    
    context = {
        'form': form,
    }
    return render(request, 'cuentas/registrarse.html', context)


def login(request):
    
    return render(request, 'cuentas/login.html')


def logout(request):
    
    return render(request, 'cuentas/logout.html')