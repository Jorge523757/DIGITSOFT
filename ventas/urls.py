"""
DigitSoft - Módulo de Ventas
URLs

Define las rutas del módulo de gestión de ventas.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    # Dashboard de ventas
    path('', views.lista_ventas, name='lista'),
]
