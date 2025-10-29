"""
DigitSoft - Módulo de Ventas
Views

Define las vistas para la gestión de ventas.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_ventas(request):
    """Vista para listar ventas"""
    context = {
        'titulo': 'Gestión de Ventas',
        'seccion': 'ventas'
    }
    return render(request, 'ventas/lista.html', context)
