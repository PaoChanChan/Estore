
from django.urls import path
from . import views


urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('categoria/<slug:categoria_slug>/', views.tienda, name='productos_por_categoria'),
    path('categoria/<slug:categoria_slug>/<slug:producto_slug>/', views.detalle_producto, name='detalle_producto'),
    path('search/', views.search, name='search'),
    path('publicar_opinion/<int:id_producto>/', views.publicar_opinion, name='publicar_opinion'),

]
