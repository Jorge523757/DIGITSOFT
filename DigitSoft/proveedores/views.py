"""
DigitSoft - Módulo de Proveedores
Views

Define las vistas para la gestión de proveedores.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_proveedores(request):
    """Vista para listar proveedores"""
    context = {
        'titulo': 'Gestión de Proveedores',
        'seccion': 'proveedores'
    }
    return render(request, 'proveedores/lista.html', context)
