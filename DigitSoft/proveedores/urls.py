"""
DigitSoft - Módulo de Proveedores
URLs

Define las rutas del módulo de gestión de proveedores.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    # Dashboard de proveedores
    path('', views.lista_proveedores, name='lista'),
]
