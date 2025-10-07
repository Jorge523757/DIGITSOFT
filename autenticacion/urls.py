from django.urls import path
from . import views

app_name = 'autenticacion'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_publico_view, name='registro_publico'),

    # Perfil de Usuario
    path('perfil/', views.perfil_usuario_view, name='perfil_usuario'),
    path('perfil/cambiar-password/', views.cambiar_password_view, name='cambiar_password'),

    # Recuperación de contraseña
    path('recuperar-password/', views.recuperar_password_view, name='recuperar_password'),
    path('verificar-codigo/', views.verificar_codigo_view, name='verificar_codigo'),
    path('nueva-password/', views.nueva_password_view, name='nueva_password'),

    # Gestión de usuarios (solo administradores)
    path('admin/registro/', views.registro_usuario_view, name='registro'),
    path('usuarios/', views.lista_usuarios_view, name='lista_usuarios'),
    path('usuarios/<int:user_id>/toggle/', views.toggle_estado_usuario, name='toggle_estado_usuario'),
]
