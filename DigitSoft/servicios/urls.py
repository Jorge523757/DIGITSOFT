"""
DigitSoft - Módulo de Servicios
URLs

Define las rutas del módulo de gestión de servicios.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    # Dashboard de servicios
    path('', views.lista_servicios, name='lista'),
]
