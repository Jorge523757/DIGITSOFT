"""
DigitSoft - Sistema de Gestión Empresarial
URL Configuration

Este archivo define las rutas principales del proyecto DigitSoft.
Organiza los módulos de forma modular y escalable.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ============================================================================
# CONFIGURACIÓN DE RUTAS PRINCIPALES
# ============================================================================

urlpatterns = [
    # Panel de Administración de Django
    path('admin/', admin.site.urls),

    # ========================================================================
    # MÓDULO PRINCIPAL
    # ========================================================================
    path('', include('DigitSoft.urls')),

    # ========================================================================
    # MÓDULOS DE GESTIÓN Y AUTENTICACIÓN
    # ========================================================================
    path('administrador/', include('administrador.urls')),
    path('autenticacion/', include('autenticacion.urls')),

    # ========================================================================
    # MÓDULOS DE NEGOCIO
    # ========================================================================
    # Gestión de Clientes
    path('clientes/', include('clientes.urls')),

    # Gestión de Proveedores
    path('proveedores/', include('proveedores.urls')),

    # Gestión de Inventario
    path('inventario/', include('inventario.urls')),

    # ========================================================================
    # MÓDULOS DE OPERACIONES
    # ========================================================================
    # Gestión de Ventas
    path('ventas/', include('ventas.urls')),

    # Gestión de Servicios
    path('servicios/', include('servicios.urls')),
]

# ============================================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y MEDIA
# ============================================================================
# Servir archivos de media solo en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
