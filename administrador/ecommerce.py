"""
Módulo E-Commerce - Digit Soft
Sistema completo de tienda online con carrito, facturación y garantías
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal


def calcular_totales_carrito(items_carrito):
    """Calcula los totales del carrito"""
    subtotal = sum(item.producto.precio_venta * item.cantidad for item in items_carrito)
    iva = subtotal * Decimal('0.19')  # 19% IVA
    total = subtotal + iva
    
    return {
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'cantidad_items': sum(item.cantidad for item in items_carrito)
    }


def verificar_stock_disponible(producto, cantidad):
    """Verifica si hay stock disponible para un producto"""
    return producto.stock_actual >= cantidad


def reducir_stock_producto(producto, cantidad):
    """Reduce el stock de un producto después de una venta"""
    if verificar_stock_disponible(producto, cantidad):
        producto.stock_actual -= cantidad
        producto.save()
        return True
    return False


def generar_numero_venta():
    """Genera un número único de venta"""
    from administrador.models import Venta
    from django.utils import timezone
    
    fecha = timezone.now().strftime('%Y%m%d')
    ultimo = Venta.objects.filter(numero_venta__startswith=f'V{fecha}').count()
    return f'V{fecha}{(ultimo + 1):04d}'


def generar_numero_factura():
    """Genera un número único de factura"""
    from administrador.models import Factura
    from django.utils import timezone
    
    fecha = timezone.now().strftime('%Y%m%d')
    ultimo = Factura.objects.filter(numero_factura__startswith=f'F{fecha}').count()
    return f'F{fecha}{(ultimo + 1):04d}'


def generar_numero_garantia():
    """Genera un número único de garantía"""
    from administrador.models import Garantia
    from django.utils import timezone
    
    fecha = timezone.now().strftime('%Y%m%d')
    ultimo = Garantia.objects.filter(numero_garantia__startswith=f'G{fecha}').count()
    return f'G{fecha}{(ultimo + 1):04d}'


# ========================================================================
# VISTAS DE E-COMMERCE
# ========================================================================

@login_required
def tienda_publica(request):
    """Vista pública de la tienda online"""
    from .models import Producto

    productos = Producto.objects.filter(activo=True, stock_actual__gt=0)

    # Filtros
    categoria = request.GET.get('categoria')
    busqueda = request.GET.get('q')

    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    context = {
        'titulo': 'Tienda Online',
        'productos': productos,
        'seccion': 'tienda'
    }
    return render(request, 'administrador/tienda_publica.html', context)


@login_required
def ver_carrito(request):
    """Vista del carrito de compras del usuario"""
    from .models import Carrito, ItemCarrito

    # Obtener o crear carrito del usuario
    carrito, created = Carrito.objects.get_or_create(
        cliente=request.user,
        estado='ACTIVO'
    )

    items = ItemCarrito.objects.filter(carrito=carrito).select_related('producto')
    totales = calcular_totales_carrito(items)

    context = {
        'titulo': 'Mi Carrito',
        'carrito': carrito,
        'items': items,
        'totales': totales,
        'seccion': 'carrito'
    }
    return render(request, 'administrador/ver_carrito.html', context)


@login_required
def mis_compras(request):
    """Vista de compras del usuario"""
    from .models import Venta

    compras = Venta.objects.filter(cliente=request.user).order_by('-fecha_venta')

    context = {
        'titulo': 'Mis Compras',
        'compras': compras,
        'seccion': 'mis_compras'
    }
    return render(request, 'administrador/mis_compras.html', context)
