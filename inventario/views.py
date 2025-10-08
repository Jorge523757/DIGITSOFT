"""
DigitSoft - Módulo de Inventario
Views

Define las vistas para la gestión de inventario.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_inventario(request):
    """Vista para listar inventario"""
    context = {
        'titulo': 'Gestión de Inventario',
        'seccion': 'inventario'
    }
    return render(request, 'inventario/lista.html', context)
