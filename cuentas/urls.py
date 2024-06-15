from django.urls import path
from . import views


urlpatterns = [
    path('registrarse/', views.registrarse, name= 'registrarse'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_productos/', views.seller_productos, name='seller_productos'),
    path('', views.dashboard, name= 'dashboard'),
    
    
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_password/', views.cambiar_password, name='cambiar_password'),
    path('detalle_pedido/<int:id_pedido>/', views.detalle_pedido, name='detalle_pedido'),

]