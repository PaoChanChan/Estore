from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cuenta

# Register your models here.

class AdminCuenta(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'username', 'fecha_inscripcion', 'ultimo_acceso', 'is_active')
    list_display_links = ('email', 'nombre', 'apellido')
    readonly_fields = ('ultimo_acceso', 'fecha_inscripcion')
    ordering = ('fecha_inscripcion',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    

admin.site.register(Cuenta, AdminCuenta)