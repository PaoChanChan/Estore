from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Import que habilita la cuenta de manager

# Create your models here.

class CuentaManager(BaseUserManager):
    def create_user(self, nombre, apellido, username, email, telefono, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        if not username:
            raise ValueError('Se requiere un nombre de usuario')

        user = self.model(
            email = self.normalize_email(email), #  Normalizar el email antes de meterlo en la db (mayúsculas, etc)
            username = username,
            nombre = nombre,
            apellido = apellido,
            telefono = telefono
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, nombre, apellido, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            nombre = nombre,
            apellido = apellido,
            password = password
        )
        user.is_admin = True
        user.is_active  = True
        user.is_staff = True
        user.is_superadmin = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
class Cuenta(AbstractBaseUser):
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=100)
    telefono = models.CharField(max_length=50)
    
    # Requerimientos:
    
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido']
    
    objects = CuentaManager()
    
    def full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        #  Método que se utiliza en Django para determinar si un usuario tiene un permiso específico
        return self.is_admin
    
    def has_module_perms(self, add_label):
        #  Método que se utiliza para determinar si un usuario tiene permisos para acceder a un módulo específico en la aplicación
        return True
    
class PerfilUsuario(models.Model):
    
    usuario = models.OneToOneField(Cuenta, on_delete=models.CASCADE)
    direccion_1 = models.CharField(blank=True, max_length=100)
    direccion_2 = models.CharField(blank=True, max_length=100)
    foto_perfil = models.ImageField(blank=True, upload_to='perfilusuario/')
    ciudad = models.CharField(blank=True, max_length=20)
    municipio = models.CharField(blank=True, max_length=20)
    pais = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.usuario.nombre

    def full_address(self):
        return f'{self.direccion_1} {self.direccion_2}'
