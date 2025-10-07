"""
Módulo E-Commerce - Digit Soft
Sistema completo de tienda online con carrito, facturación y garantías
"""
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

