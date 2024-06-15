from django.urls import path
from . import views

urlpatterns = [
    path('hacer_pedido/', views.hacer_pedido, name='hacer_pedido'),
    path('pago/', views.pago, name='pago'),
    #path('pedido_completado/', views.pedido_completado, name='pedido_completado'),
]