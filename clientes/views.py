"""
DigitSoft - Módulo de Clientes
Views

Define las vistas para la gestión de clientes.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lista_clientes(request):
    """Vista para listar clientes"""
    context = {
        'titulo': 'Gestión de Clientes',
        'seccion': 'clientes'
    }
    return render(request, 'clientes/lista.html', context)

