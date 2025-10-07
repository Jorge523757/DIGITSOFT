from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from administrador.models import Producto, Marca

def home(request):
    """Vista para la página principal"""
    context = {
        'page_title': 'Inicio - Digit Soft',
        'meta_description': 'Proporcionamos soluciones integrales que transforman la experiencia digital de empresas',
    }
    return render(request, 'DigitSoft/home.html', context)

def pagina_principal(request):
    """Vista para la página principal pública con ecommerce digital"""
    # Obtener productos destacados y activos
    productos_destacados = Producto.objects.filter(
        activo=True,
        stock_actual__gt=0
    ).select_related('marca').order_by('-fecha_registro')[:8]

    # Obtener todas las marcas activas
    marcas = Marca.objects.filter(activa=True)

    # Obtener categorías únicas de productos
    categorias = Producto.objects.filter(activo=True).values_list('categoria', flat=True).distinct()

    context = {
        'page_title': 'Digit Soft - Soluciones Integrales Digitales',
        'meta_description': 'Proporcionamos soluciones integrales que transforman la experiencia digital de empresas',
        'productos_destacados': productos_destacados,
        'marcas': marcas,
        'categorias': categorias,
    }
    return render(request, 'DigitSoft/pagina_principal.html', context)

def tienda(request):
    """Vista para la tienda online con carrito de compras"""
    # Obtener parámetros de filtrado
    categoria_filter = request.GET.get('categoria', '')
    marca_filter = request.GET.get('marca', '')
    search_query = request.GET.get('search', '')

    # Obtener productos activos
    productos = Producto.objects.filter(activo=True, stock_actual__gt=0).select_related('marca')

    # Aplicar filtros
    if categoria_filter:
        productos = productos.filter(categoria=categoria_filter)
    if marca_filter:
        productos = productos.filter(marca__id=marca_filter)
    if search_query:
        productos = productos.filter(nombre__icontains=search_query)

    # Obtener marcas y categorías para los filtros
    marcas = Marca.objects.filter(activa=True)
    categorias = Producto.objects.filter(activo=True).values('categoria').distinct()

    context = {
        'page_title': 'Tienda - Digit Soft',
        'meta_description': 'Tienda online de productos y servicios digitales',
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'categoria_selected': categoria_filter,
        'marca_selected': marca_filter,
        'search_query': search_query,
    }
    return render(request, 'DigitSoft/tienda.html', context)

def producto_detalle(request, producto_id):
    """Vista para ver el detalle de un producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        activo=True
    ).exclude(id=producto_id).select_related('marca')[:4]

    context = {
        'page_title': f'{producto.nombre} - Digit Soft',
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'DigitSoft/producto_detalle.html', context)

@require_POST
def agregar_al_carrito(request):
    """API para agregar productos al carrito"""
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 1))

        producto = get_object_or_404(Producto, id=producto_id, activo=True)

        # Obtener o crear el carrito en la sesión
        carrito = request.session.get('carrito', {})

        # Agregar o actualizar producto en el carrito
        producto_key = str(producto_id)
        if producto_key in carrito:
            carrito[producto_key]['cantidad'] += cantidad
        else:
            carrito[producto_key] = {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio_venta),
                'cantidad': cantidad,
                'imagen': producto.imagen.url if producto.imagen else None,
            }

        # Verificar stock
        if carrito[producto_key]['cantidad'] > producto.stock_actual:
            carrito[producto_key]['cantidad'] = producto.stock_actual

        request.session['carrito'] = carrito
        request.session.modified = True

        # Calcular total de items
        total_items = sum(item['cantidad'] for item in carrito.values())

        return JsonResponse({
            'success': True,
            'message': 'Producto agregado al carrito',
            'total_items': total_items,
            'carrito': carrito
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
def actualizar_carrito(request):
    """API para actualizar la cantidad de un producto en el carrito"""
    try:
        data = json.loads(request.body)
        producto_id = str(data.get('producto_id'))
        cantidad = int(data.get('cantidad', 1))

        carrito = request.session.get('carrito', {})

        if producto_id in carrito:
            if cantidad <= 0:
                del carrito[producto_id]
            else:
                carrito[producto_id]['cantidad'] = cantidad

        request.session['carrito'] = carrito
        request.session.modified = True

        # Calcular totales
        total_items = sum(item['cantidad'] for item in carrito.values())
        subtotal = sum(item['precio'] * item['cantidad'] for item in carrito.values())

        return JsonResponse({
            'success': True,
            'total_items': total_items,
            'subtotal': subtotal,
            'carrito': carrito
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
def eliminar_del_carrito(request):
    """API para eliminar un producto del carrito"""
    try:
        data = json.loads(request.body)
        producto_id = str(data.get('producto_id'))

        carrito = request.session.get('carrito', {})

        if producto_id in carrito:
            del carrito[producto_id]

        request.session['carrito'] = carrito
        request.session.modified = True

        total_items = sum(item['cantidad'] for item in carrito.values())

        return JsonResponse({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'total_items': total_items,
            'carrito': carrito
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def ver_carrito(request):
    """Vista para ver el carrito de compras"""
    carrito = request.session.get('carrito', {})

    # Calcular totales
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    iva = subtotal * 0.19  # 19% IVA
    total = subtotal + iva

    context = {
        'page_title': 'Carrito de Compras - Digit Soft',
        'carrito': carrito,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    }
    return render(request, 'DigitSoft/carrito.html', context)

def checkout(request):
    """Vista para el proceso de checkout"""
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('main:tienda')

    # Calcular totales
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    iva = subtotal * 0.19
    total = subtotal + iva

    context = {
        'page_title': 'Finalizar Compra - Digit Soft',
        'carrito': carrito,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    }
    return render(request, 'DigitSoft/checkout.html', context)

def portafolio(request):
    """Vista para la página de portafolio"""
    context = {
        'page_title': 'Portafolio - Digit Soft',
    }
    return render(request, 'DigitSoft/portafolio.html', context)

def servicios(request):
    """Vista para la página de servicios"""
    context = {
        'page_title': 'Servicios - Digit Soft',
    }
    return render(request, 'DigitSoft/servicios.html', context)

def diseno_web(request):
    """Vista para la página de paquetes de diseño web"""
    context = {
        'page_title': 'Diseño Web - Digit Soft',
    }
    return render(request, 'DigitSoft/diseno_web.html', context)

def nosotros(request):
    """Vista para la página nosotros"""
    context = {
        'page_title': 'Nosotros - Digit Soft',
    }
    return render(request, 'DigitSoft/nosotros.html', context)

def contacto(request):
    """Vista para la página de contacto"""
    context = {
        'page_title': 'Contacto - Digit Soft',
    }
    return render(request, 'DigitSoft/contacto.html', context)

def dashboard(request):
    """Vista para el dashboard principal"""
    context = {
        'page_title': 'Dashboard - Digit Soft',
    }
    return render(request, 'DigitSoft/dashboard.html', context)
