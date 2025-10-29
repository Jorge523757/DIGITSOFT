"""
DigitSoft - Módulo de Clientes
URLs

Define las rutas del módulo de gestión de clientes.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    # Dashboard de clientes
    path('', views.lista_clientes, name='lista'),
]

