from django import forms
from .models import Cuenta, PerfilUsuario
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Introducir contraseña',
        'class': 'form-control'
    }))
    
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar contraseña',
        'class': 'form-control'
    }))
    
    class Meta:
        model = Cuenta
        fields = ['nombre', 'apellido', 'email', 'password', 'telefono']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cuenta.objects.filter(email=email).exists():
            raise ValidationError('El email ya está registrado.')
        return email
        
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if password != confirmar_password:
            raise ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre'
        self.fields['apellido'].widget.attrs['placeholder'] = 'Apellido'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Teléfono'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

            
   
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('direccion_1', 'direccion_2', 'ciudad', 'municipio', 'pais', 'foto_perfil')

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'