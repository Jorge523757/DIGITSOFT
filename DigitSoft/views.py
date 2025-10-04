from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    """Vista para la página principal"""
    context = {
        'page_title': 'Inicio - Digit Soft',
        'meta_description': 'Proporcionamos soluciones integrales que transforman la experiencia digital de empresas',
    }
    return render(request, 'DigitSoft/home.html', context)

def pagina_principal(request):
    """Vista para el módulo de página principal del dashboard"""
    context = {
        'page_title': 'Página Principal - Digit Soft',
        'meta_description': 'Página principal del sistema de gestión Digit Soft',
    }
    return render(request, 'DigitSoft/pagina_principal.html', context)

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
