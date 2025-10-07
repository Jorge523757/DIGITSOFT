"""
Decoradores personalizados para control de acceso por tipo de usuario
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    """
    Decorador que permite acceso solo a Super Administradores y Administradores
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.tipo_usuario in ['SUPER_ADMIN', 'ADMINISTRADOR']:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('main:pagina_principal')
        except:
            messages.error(request, 'No tienes un perfil válido.')
            return redirect('main:pagina_principal')
    return wrapper


def cliente_required(view_func):
    """
    Decorador que permite acceso solo a Clientes
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.tipo_usuario == 'CLIENTE':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Esta sección es solo para clientes.')
                return redirect('administrador:dashboard')
        except:
            messages.error(request, 'No tienes un perfil válido.')
            return redirect('main:pagina_principal')
    return wrapper


def tecnico_required(view_func):
    """
    Decorador que permite acceso solo a Técnicos
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.tipo_usuario == 'TECNICO':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Esta sección es solo para técnicos.')
                return redirect('main:pagina_principal')
        except:
            messages.error(request, 'No tienes un perfil válido.')
            return redirect('main:pagina_principal')
    return wrapper


def proveedor_required(view_func):
    """
    Decorador que permite acceso solo a Proveedores
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            perfil = request.user.perfil
            if perfil.tipo_usuario == 'PROVEEDOR':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Esta sección es solo para proveedores.')
                return redirect('main:pagina_principal')
        except:
            messages.error(request, 'No tienes un perfil válido.')
            return redirect('main:pagina_principal')
    return wrapper


def tipo_usuario_required(*tipos_permitidos):
    """
    Decorador flexible que permite especificar múltiples tipos de usuario
    Uso: @tipo_usuario_required('CLIENTE', 'ADMINISTRADOR')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            try:
                perfil = request.user.perfil
                if perfil.tipo_usuario in tipos_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'No tienes permisos para acceder a esta sección.')
                    # Redirigir según tipo de usuario
                    if perfil.tipo_usuario in ['SUPER_ADMIN', 'ADMINISTRADOR']:
                        return redirect('administrador:dashboard')
                    else:
                        return redirect('main:pagina_principal')
            except:
                messages.error(request, 'No tienes un perfil válido.')
                return redirect('main:pagina_principal')
        return wrapper
    return decorator

