"""
DigitSoft - Módulo de Servicios
Views

Define las vistas para la gestión de servicios.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_servicios(request):
    """Vista para listar servicios"""
    context = {
        'titulo': 'Gestión de Servicios',
        'seccion': 'servicios'
    }
    return render(request, 'servicios/lista.html', context)
