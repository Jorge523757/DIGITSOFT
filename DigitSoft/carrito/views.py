from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Carrito
from cliente.models import Cliente

def lista_carritos(request):
    """Vista básica para listar carritos"""
    carritos = Carrito.objects.select_related('cliente', 'venta_generada').all()
    context = {
        'carritos': carritos,
        'titulo': 'Gestión de Carritos'
    }
    return render(request, 'carrito/lista.html', context)

def detalle_carrito(request, carrito_id):
    """Vista para mostrar el detalle de un carrito"""
    carrito = get_object_or_404(Carrito, id=carrito_id)
    items = carrito.items.select_related('producto').all() if hasattr(carrito, 'items') else []

    context = {
        'carrito': carrito,
        'items': items,
        'titulo': f'Carrito #{carrito.id}'
    }
    return render(request, 'carrito/detalle.html', context)

@require_POST
def actualizar_estado_carrito(request, carrito_id):
    """Vista para actualizar el estado de un carrito"""
    carrito = get_object_or_404(Carrito, id=carrito_id)
    nuevo_estado = request.POST.get('estado')

    if nuevo_estado in dict(Carrito.ESTADO_CHOICES):
        carrito.estado = nuevo_estado
        carrito.save()
        messages.success(request, f'Estado del carrito actualizado a {carrito.get_estado_display()}')
    else:
        messages.error(request, 'Estado no válido')

    return redirect('carrito:detalle', carrito_id=carrito.id)

def carritos_abandonados(request):
    """Vista para mostrar carritos abandonados"""
    carritos = Carrito.objects.filter(estado='ABANDONADO').select_related('cliente')
    context = {
        'carritos': carritos,
        'titulo': 'Carritos Abandonados'
    }
    return render(request, 'carrito/abandonados.html', context)
