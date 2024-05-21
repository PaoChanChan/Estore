from django.urls import path
from . import views


urlpatterns = [
    path('registrarse/', views.registrarse, name= 'registrarse'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),

]