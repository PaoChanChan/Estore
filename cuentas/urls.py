from django.urls import path
from . import views


urlpatterns = [
    path('registrarse/', views.registrarse, name= 'registrarse'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('', views.dashboard, name= 'dashboard'),
    
    
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('detalle_pedido/<int:id_pedido>/', views.detalle_pedido, name='detalle_pedido'),

]