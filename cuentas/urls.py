from django.urls import path
from . import views


urlpatterns = [
    path('registrarse/', views.registrarse, name= 'registrarse'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('', views.dashboard, name= 'dashboard'),
    
    path('activar/<uidb64>/<token>/', views.activar, name='activar'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validar/<uidb64>/<token>/', views.resetpassword_validar, name='resetpassword_validar'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

]