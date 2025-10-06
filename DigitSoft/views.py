from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from administrador.models import Producto

def home(request):
    """Vista para la página principal"""
    context = {
        'page_title': 'Inicio - Digit Soft',
        'meta_description': 'Proporcionamos soluciones integrales que transforman la experiencia digital de empresas',
    }
    return render(request, 'DigitSoft/home.html', context)

def pagina_principal(request):
    """Vista para la página principal pública con ecommerce digital"""
    # Obtener productos activos para la tienda digital
    productos = Producto.objects.filter(activo=True).select_related('marca')

    # Convertir productos a JSON para JavaScript
    productos_list = []
    for p in productos:
        productos_list.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion or 'Producto de calidad',
            'categoria': p.categoria,
            'categoria_display': p.get_categoria_display(),
            'precio_venta': float(p.precio_venta),
            'stock_actual': p.stock_actual,
            'imagen': p.imagen.url if p.imagen else None,
            'marca': p.marca.nombre if p.marca else 'Digit Soft'
        })

    context = {
        'page_title': 'Digit Soft - Soluciones Integrales Digitales',
        'meta_description': 'Proporcionamos soluciones integrales que transforman la experiencia digital de empresas',
        'productos_json': json.dumps(productos_list),
    }
    return render(request, 'DigitSoft/pagina_principal.html', context)

def tienda(request):
    """Vista para la tienda online con carrito de compras"""
    # Obtener productos activos
    productos = Producto.objects.filter(activo=True).select_related('marca')

    # Convertir productos a JSON para JavaScript
    productos_list = []
    for p in productos:
        productos_list.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion or '',
            'categoria': p.categoria,
            'precio_venta': float(p.precio_venta),
            'imagen': p.imagen.url if p.imagen else None,
            'marca': p.marca.nombre if p.marca else 'Sin marca'
        })

    context = {
        'page_title': 'Tienda - Digit Soft',
        'meta_description': 'Tienda online de productos y servicios digitales',
        'productos_json': json.dumps(productos_list),
    }
    return render(request, 'DigitSoft/tienda.html', context)

def portafolio(request):
    """Vista para la página de portafolio"""
    context = {
        'page_title': 'Portafolio - Digit Soft',
    }
    return render(request, 'portafolio.html', context)

def servicios(request):
    """Vista para la página de servicios"""
    context = {
        'page_title': 'Servicios - Digit Soft',
    }
    return render(request, 'servicios.html', context)

def nosotros(request):
    """Vista para la página nosotros"""
    context = {
        'page_title': 'Nosotros - Digit Soft',
    }
    return render(request, 'nosotros.html', context)

def contacto(request):
    """Vista para la página de contacto"""
    context = {
        'page_title': 'Contacto - Digit Soft',
    }
    return render(request, 'contacto.html', context)

def dashboard(request):
    """Vista para el dashboard principal"""
    context = {
        'page_title': 'Dashboard - Digit Soft',
    }
    return render(request, 'DigitSoft/dashboard.html', context)
