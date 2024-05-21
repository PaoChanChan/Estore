from django import forms
from .models import Cuenta


class RegistroForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Introducir contraseña',
    }))
    
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirmar contraseña'
    }))
    
    class Meta:
        model = Cuenta
        fields = ['nombre', 'apellido', 'email', 'telefono', 'password']
        
    def __init__(self, *args, **kwargs):
        """Función que aplica el estilo del formulario a cada campo de texto"""
        
        #   El uso de super permitirá en algún momento modificar la forma en la que se almacenan los datos a través del django admin.
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre'
        self.fields['apellido'].widget.attrs['placeholder'] = 'Apellido'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Teléfono'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    def clean(self):
        """Función para verificar que la contraseña y su confirmación son las mismas """
        
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if password != confirmar_password:
            raise forms.ValidationError(
                'Las contraseñas no coinciden'
            )
        