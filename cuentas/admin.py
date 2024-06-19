from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cuenta, PerfilUsuario
from django.utils.html import format_html

# Register your models here.

class AdminCuenta(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'username', 'fecha_inscripcion', 'ultimo_acceso', 'is_active')
    list_display_links = ('email', 'nombre', 'apellido')
    readonly_fields = ('ultimo_acceso', 'fecha_inscripcion')
    ordering = ('fecha_inscripcion',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class PerfilUsuarioAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.foto_perfil.url))
    list_display = ('usuario', 'ciudad', 'municipio', 'pais')

admin.site.register(Cuenta, AdminCuenta)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)