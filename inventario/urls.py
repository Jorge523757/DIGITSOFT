"""
DigitSoft - Módulo de Inventario
URLs

Define las rutas del módulo de gestión de inventario.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Dashboard de inventario
    path('', views.lista_inventario, name='lista'),
]
