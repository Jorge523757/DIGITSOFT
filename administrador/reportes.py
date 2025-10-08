"""
Módulo de Reportes - Digit Soft
Sistema de generación de reportes en PDF y Excel
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
import csv
from autenticacion.decorators import admin_required


# ========================================================================
# VISTAS DE REPORTES
# ========================================================================

@login_required
@admin_required
def reportes_dashboard(request):
    """Vista principal del dashboard de reportes"""
    context = {
        'titulo': 'Dashboard de Reportes',
        'seccion': 'reportes'
    }
    return render(request, 'administrador/reportes_dashboard.html', context)


@login_required
@admin_required
def reporte_ventas(request):
    """Vista del reporte de ventas"""
    context = {
        'titulo': 'Reporte de Ventas',
        'seccion': 'reportes'
    }
    return render(request, 'administrador/reporte_ventas.html', context)


@login_required
@admin_required
def reporte_inventario(request):
    """Vista del reporte de inventario"""
    try:
        from .models import Producto
        productos = Producto.objects.all()
        productos_bajo_stock = productos.filter(stock_actual__lte=5)
    except:
        productos = []
        productos_bajo_stock = []

    context = {
        'titulo': 'Reporte de Inventario',
        'seccion': 'reportes',
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock
    }
    return render(request, 'administrador/reporte_inventario.html', context)


@login_required
@admin_required
def reporte_servicios(request):
    """Vista del reporte de servicios"""
    context = {
        'titulo': 'Reporte de Servicios',
        'seccion': 'reportes'
    }
    return render(request, 'administrador/reporte_servicios.html', context)
