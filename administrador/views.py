from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Cliente, Tecnico, Marca, Proveedor, Producto,
    Equipo, ServicioTecnico, OrdenServicio, Compra, Carrito,
    Venta, Garantia, Factura, Administrador
)
from .forms import (
    ProductoForm, ClienteForm, ProveedorForm, MarcaForm, EquipoForm,
    TecnicoForm, OrdenServicioForm, VentaForm, CompraForm,
    GarantiaForm, ServicioTecnicoForm
)

# ========== DASHBOARD ========== #
def dashboard(request):
    """Vista principal del dashboard del administrador"""
    stats = {
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_productos': Producto.objects.filter(activo=True).count(),
        'ordenes_pendientes': OrdenServicio.objects.filter(estado='PENDIENTE').count(),
        'ventas_mes': Venta.objects.filter(fecha_venta__month=timezone.now().month).count(),
        'equipos_reparacion': Equipo.objects.filter(estado_fisico='EN_REPARACION').count(),
        'tecnicos_disponibles': Tecnico.objects.filter(estado_actual='DISPONIBLE').count(),
    }

    ordenes_recientes = OrdenServicio.objects.select_related('cliente', 'tecnico_asignado')[:5]
    productos_stock_bajo = Producto.objects.filter(stock_actual__lte=F('stock_minimo'))[:5]

    context = {
        'stats': stats,
        'ordenes_recientes': ordenes_recientes,
        'productos_stock_bajo': productos_stock_bajo,
        'titulo': 'Dashboard - DigitSoft'
    }
    return render(request, 'administrador/dashboard.html', context)

# ========== PRODUCTOS ========== #
def producto_list(request):
    """Vista para listar y crear productos"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" registrado correctamente.')
            return redirect('administrador:producto_list')
        else:
            messages.error(request, 'Error al guardar el producto. Verifica los datos.')
    else:
        form = ProductoForm()

    productos = Producto.objects.select_related('marca', 'proveedor_principal').filter(activo=True)

    context = {
        'productos': productos,
        'form': form,
        'titulo': 'Gestión de Productos'
    }
    return render(request, 'administrador/producto_list.html', context)

def producto_detail(request, producto_id):
    """Vista de detalle de producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    context = {
        'producto': producto,
        'titulo': f'Producto: {producto.nombre}'
    }
    return render(request, 'administrador/producto_detail.html', context)

def producto_edit(request, producto_id):
    """Vista para editar producto"""
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('administrador:producto_list')
        else:
            messages.error(request, 'Error al actualizar el producto.')
    else:
        form = ProductoForm(instance=producto)

    context = {
        'form': form,
        'producto': producto,
        'titulo': f'Editar: {producto.nombre}'
    }
    return render(request, 'administrador/producto_form.html', context)

def producto_delete(request, producto_id):
    """Vista para eliminar producto (soft delete)"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        producto.activo = False
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
    return redirect('administrador:producto_list')

# ========== CLIENTES ========== #
def cliente_list(request):
    """Vista para listar y crear clientes"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombres}" registrado correctamente.')
            return redirect('administrador:cliente_list')
        else:
            messages.error(request, 'Error al guardar el cliente. Verifica los datos.')
    else:
        form = ClienteForm()

    clientes = Cliente.objects.filter(activo=True)

    context = {
        'clientes': clientes,
        'form': form,
        'titulo': 'Gestión de Clientes'
    }
    return render(request, 'administrador/cliente_list.html', context)

def cliente_detail(request, cliente_id):
    """Vista de detalle de cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    context = {
        'cliente': cliente,
        'titulo': f'Cliente: {cliente.nombres} {cliente.apellidos}'
    }
    return render(request, 'administrador/cliente_detail.html', context)

def cliente_delete(request, cliente_id):
    """Vista para eliminar cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.activo = False
        cliente.save()
        messages.success(request, f'Cliente "{cliente.nombres}" eliminado correctamente.')
    return redirect('administrador:cliente_list')

# ========== PROVEEDORES ========== #
def proveedor_list(request):
    """Vista para listar y crear proveedores"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.razon_social}" registrado correctamente.')
            return redirect('administrador:proveedor_list')
        else:
            messages.error(request, 'Error al guardar el proveedor. Verifica los datos.')
    else:
        form = ProveedorForm()

    proveedores = Proveedor.objects.filter(activo=True)

    context = {
        'proveedores': proveedores,
        'form': form,
        'titulo': 'Gestión de Proveedores'
    }
    return render(request, 'administrador/proveedor_list.html', context)

def proveedor_detail(request, proveedor_id):
    """Vista de detalle de proveedor"""
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    context = {
        'proveedor': proveedor,
        'titulo': f'Proveedor: {proveedor.razon_social}'
    }
    return render(request, 'administrador/proveedor_detail.html', context)

def proveedor_delete(request, proveedor_id):
    """Vista para eliminar proveedor"""
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        proveedor.activo = False
        proveedor.save()
        messages.success(request, f'Proveedor "{proveedor.razon_social}" eliminado correctamente.')
    return redirect('administrador:proveedor_list')

# ========== MARCAS ========== #
def marca_list(request):
    """Vista para listar y crear marcas"""
    if request.method == 'POST':
        form = MarcaForm(request.POST, request.FILES)
        if form.is_valid():
            marca = form.save()
            messages.success(request, f'Marca "{marca.nombre}" registrada correctamente.')
            return redirect('administrador:marca_list')
        else:
            messages.error(request, 'Error al guardar la marca. Verifica los datos.')
    else:
        form = MarcaForm()

    marcas = Marca.objects.filter(activa=True)

    context = {
        'marcas': marcas,
        'form': form,
        'titulo': 'Gestión de Marcas'
    }
    return render(request, 'administrador/marca_list.html', context)

def marca_detail(request, marca_id):
    """Vista de detalle de marca"""
    marca = get_object_or_404(Marca, id=marca_id)
    productos_marca = Producto.objects.filter(marca=marca, activo=True)
    context = {
        'marca': marca,
        'productos_marca': productos_marca,
        'titulo': f'Marca: {marca.nombre}'
    }
    return render(request, 'administrador/marca_detail.html', context)

def marca_delete(request, marca_id):
    """Vista para eliminar marca"""
    if request.method == 'POST':
        marca = get_object_or_404(Marca, id=marca_id)
        marca.activa = False
        marca.save()
        messages.success(request, f'Marca "{marca.nombre}" eliminada correctamente.')
    return redirect('administrador:marca_list')

# ========== EQUIPOS ========== #
def equipo_list(request):
    """Vista para listar y crear equipos"""
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save()
            messages.success(request, f'Equipo "{equipo.nombre}" registrado correctamente.')
            return redirect('administrador:equipo_list')
        else:
            messages.error(request, 'Error al guardar el equipo. Verifica los datos.')
    else:
        form = EquipoForm()

    equipos = Equipo.objects.select_related('cliente', 'marca').filter(activo=True)

    context = {
        'equipos': equipos,
        'form': form,
        'titulo': 'Gestión de Equipos'
    }
    return render(request, 'administrador/equipo_list.html', context)

def equipo_detail(request, equipo_id):
    """Vista de detalle de equipo"""
    equipo = get_object_or_404(Equipo, id=equipo_id)
    context = {
        'equipo': equipo,
        'titulo': f'Equipo: {equipo.nombre}'
    }
    return render(request, 'administrador/equipo_detail.html', context)

def equipo_delete(request, equipo_id):
    """Vista para eliminar equipo"""
    if request.method == 'POST':
        equipo = get_object_or_404(Equipo, id=equipo_id)
        equipo.activo = False
        equipo.save()
        messages.success(request, f'Equipo "{equipo.nombre}" eliminado correctamente.')
    return redirect('administrador:equipo_list')

# ========== TÉCNICOS ========== #
def tecnico_list(request):
    """Vista para listar y crear técnicos"""
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            tecnico = form.save()
            messages.success(request, f'Técnico "{tecnico.nombres}" registrado correctamente.')
            return redirect('administrador:tecnico_list')
        else:
            messages.error(request, 'Error al guardar el técnico. Verifica los datos.')
    else:
        form = TecnicoForm()

    tecnicos = Tecnico.objects.filter(activo=True).order_by('apellidos', 'nombres')

    context = {
        'tecnicos': tecnicos,
        'form': form,
        'titulo': 'Gestión de Técnicos'
    }
    return render(request, 'administrador/tecnico_list.html', context)

def tecnico_detail(request, tecnico_id):
    """Vista de detalle de técnico"""
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)
    context = {
        'tecnico': tecnico,
        'titulo': f'Técnico: {tecnico.nombres} {tecnico.apellidos}'
    }
    return render(request, 'administrador/tecnico_detail.html', context)

def tecnico_delete(request, tecnico_id):
    """Vista para eliminar técnico"""
    if request.method == 'POST':
        tecnico = get_object_or_404(Tecnico, id=tecnico_id)
        tecnico.activo = False
        tecnico.save()
        messages.success(request, f'Técnico "{tecnico.nombres}" eliminado correctamente.')
    return redirect('administrador:tecnico_list')

# ========== ÓRDENES DE SERVICIO ========== #
def orden_servicio_list(request):
    """Vista para listar y crear órdenes de servicio"""
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            orden = form.save()
            messages.success(request, f'Orden de servicio #{orden.numero_orden} creada correctamente.')
            return redirect('administrador:orden_servicio_list')
        else:
            messages.error(request, 'Error al guardar la orden. Verifica los datos.')
    else:
        form = OrdenServicioForm()

    ordenes = OrdenServicio.objects.select_related('cliente', 'tecnico_asignado', 'equipo').all()

    context = {
        'ordenes': ordenes,
        'form': form,
        'titulo': 'Gestión de Órdenes de Servicio'
    }
    return render(request, 'administrador/orden_servicio_list.html', context)

def orden_servicio_detail(request, orden_id):
    """Vista de detalle de orden de servicio"""
    orden = get_object_or_404(OrdenServicio, id=orden_id)
    context = {
        'orden': orden,
        'titulo': f'Orden: {orden.numero_orden}'
    }
    return render(request, 'administrador/orden_servicio_detail.html', context)

# ========== VENTAS ========== #
def venta_list(request):
    """Vista para listar ventas"""
    ventas = Venta.objects.select_related('cliente').all()
    context = {
        'ventas': ventas,
        'titulo': 'Gestión de Ventas'
    }
    return render(request, 'administrador/venta_list.html', context)

def venta_detail(request, venta_id):
    """Vista de detalle de venta"""
    venta = get_object_or_404(Venta, id=venta_id)
    context = {
        'venta': venta,
        'titulo': f'Venta: {venta.numero_venta}'
    }
    return render(request, 'administrador/venta_detail.html', context)

# ========== COMPRAS ========== #
def compra_list(request):
    """Vista para listar compras"""
    compras = Compra.objects.select_related('proveedor').all()
    proveedores = Proveedor.objects.filter(activo=True).order_by('razon_social')
    context = {
        'compras': compras,
        'proveedores': proveedores,
        'titulo': 'Gestión de Compras'
    }
    return render(request, 'administrador/compra_list.html', context)

def compra_detail(request, compra_id):
    """Vista de detalle de compra"""
    compra = get_object_or_404(Compra, id=compra_id)
    context = {
        'compra': compra,
        'titulo': f'Compra: {compra.numero_compra}'
    }
    return render(request, 'administrador/compra_detail.html', context)

def compras_pendientes(request):
    """Vista para compras pendientes"""
    estados_pendientes = ['SOLICITUD', 'COTIZACION', 'APROBADA', 'PEDIDO_ENVIADO']
    compras = Compra.objects.filter(estado__in=estados_pendientes).select_related('proveedor')
    context = {
        'compras': compras,
        'titulo': 'Compras Pendientes'
    }
    return render(request, 'administrador/compras_pendientes.html', context)

# ========== CARRITOS ========== #
def carrito_list(request):
    """Vista para listar carritos"""
    carritos = Carrito.objects.select_related('cliente').all()
    context = {
        'carritos': carritos,
        'titulo': 'Gestión de Carritos'
    }
    return render(request, 'administrador/carrito_list.html', context)

def carrito_detail(request, carrito_id):
    """Vista de detalle de carrito"""
    carrito = get_object_or_404(Carrito, id=carrito_id)
    context = {
        'carrito': carrito,
        'titulo': f'Carrito #{carrito.id}'
    }
    return render(request, 'administrador/carrito_detail.html', context)

def carritos_abandonados(request):
    """Vista para carritos abandonados"""
    carritos = Carrito.objects.filter(estado='ABANDONADO').select_related('cliente')
    context = {
        'carritos': carritos,
        'titulo': 'Carritos Abandonados'
    }
    return render(request, 'administrador/carritos_abandonados.html', context)

# ========== GARANTÍAS ========== #
def garantia_list(request):
    """Vista para listar garantías"""
    # Obtener todas las garantías
    garantias = Garantia.objects.select_related('producto', 'equipo', 'cliente', 'venta').all()

    # Filtrar por estado si se proporciona
    estado_filtro = request.GET.get('estado')
    if estado_filtro:
        garantias = garantias.filter(estado=estado_filtro)

    # Filtrar por cliente
    cliente_id = request.GET.get('cliente')
    if cliente_id:
        garantias = garantias.filter(cliente_id=cliente_id)

    # Filtrar por vigencia
    vigencia = request.GET.get('vigencia')
    if vigencia == 'vigentes':
        from datetime import date
        garantias = garantias.filter(estado='VIGENTE', fecha_vencimiento__gte=date.today())
    elif vigencia == 'vencidas':
        from datetime import date
        garantias = garantias.filter(fecha_vencimiento__lt=date.today())

    # Ordenar por fecha de vencimiento
    garantias = garantias.order_by('-fecha_inicio')

    context = {
        'garantias': garantias,
        'titulo': 'Gestión de Garantías'
    }
    return render(request, 'administrador/garantia_list.html', context)

def garantia_detail(request, garantia_id):
    """Vista de detalle de garantía"""
    garantia = get_object_or_404(Garantia, id=garantia_id)
    context = {
        'garantia': garantia,
        'titulo': f'Garantía: {garantia.numero_garantia}'
    }
    return render(request, 'administrador/garantia_detail.html', context)

# ========== FACTURACIÓN ========== #
def facturacion_list(request):
    """Vista para listar facturas"""
    facturas = Factura.objects.select_related('cliente').all()
    context = {
        'facturas': facturas,
        'titulo': 'Gestión de Facturación'
    }
    return render(request, 'administrador/facturacion_list.html', context)

# ========== SERVICIOS TÉCNICOS ========== #
def servicio_tecnico_list(request):
    """Vista para listar servicios técnicos (catálogo)"""
    if request.method == 'POST':
        form = ServicioTecnicoForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            messages.success(request, f'Servicio "{servicio.nombre}" registrado correctamente.')
            return redirect('administrador:servicio_tecnico_list')
        else:
            messages.error(request, 'Error al guardar el servicio. Verifica los datos.')
    else:
        form = ServicioTecnicoForm()

    servicios = ServicioTecnico.objects.filter(activo=True).order_by('categoria', 'nombre')
    
    context = {
        'servicios': servicios,
        'form': form,
        'titulo': 'Catálogo de Servicios Técnicos'
    }
    return render(request, 'administrador/servicio_tecnico_list.html', context)

# ========== ADMINISTRADORES ========== #
def administrador_list(request):
    """Vista para listar administradores"""
    administradores = Administrador.objects.select_related('user').all()
    context = {
        'administradores': administradores,
        'titulo': 'Gestión de Administradores'
    }
    return render(request, 'administrador/administrador_list.html', context)

# ========== TIENDA ONLINE ========== #
def tienda_list(request):
    """Vista para gestionar productos de la tienda online"""
    productos = Producto.objects.filter(activo=True).select_related('marca', 'proveedor_principal')

    # Estadísticas de la tienda
    stats = {
        'total_productos': productos.count(),
        'productos_bajo_stock': productos.filter(stock_actual__lte=models.F('stock_minimo')).count(),
        'productos_sin_stock': productos.filter(stock_actual=0).count(),
        'valor_inventario': sum(p.precio_venta * p.stock_actual for p in productos),
    }

    context = {
        'productos': productos,
        'stats': stats,
        'titulo': 'Gestión de Tienda Online'
    }
    return render(request, 'administrador/tienda_list.html', context)

def tienda_producto_toggle(request, producto_id):
    """Vista para activar/desactivar productos en la tienda"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        producto.activo = not producto.activo
        producto.save()
        estado = "activado" if producto.activo else "desactivado"
        messages.success(request, f'Producto "{producto.nombre}" {estado} en la tienda.')
    return redirect('administrador:tienda_list')


# ========== MÓDULO DE REPORTES ========== #
from .reportes import (
    generar_reporte_ventas_csv,
    generar_reporte_inventario_csv,
    generar_reporte_clientes_csv,
    generar_reporte_servicios_csv,
    generar_reporte_compras_csv,
    obtener_estadisticas_ventas
)

def reportes_dashboard(request):
    """Dashboard principal de reportes"""
    from datetime import datetime, timedelta

    # Fecha por defecto: último mes
    fecha_fin = timezone.now()
    fecha_inicio = fecha_fin - timedelta(days=30)

    # Estadísticas generales
    stats_ventas = obtener_estadisticas_ventas(fecha_inicio, fecha_fin)

    stats = {
        'total_ventas': stats_ventas.get('total_ventas', 0),
        'total_ingresos': stats_ventas.get('total_ingresos', 0) or 0,
        'promedio_venta': stats_ventas.get('promedio_venta', 0) or 0,
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_productos': Producto.objects.filter(activo=True).count(),
        'ordenes_completadas': OrdenServicio.objects.filter(estado='COMPLETADA').count(),
        'productos_stock_bajo': Producto.objects.filter(
            stock_actual__lte=models.F('stock_minimo')
        ).count(),
    }

    context = {
        'stats': stats,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'titulo': 'Centro de Reportes'
    }
    return render(request, 'administrador/reportes_dashboard.html', context)

def reporte_ventas(request):
    """Vista para generar reporte de ventas"""
    return generar_reporte_ventas_csv(request)

def reporte_inventario(request):
    """Vista para generar reporte de inventario"""
    return generar_reporte_inventario_csv(request)

def reporte_clientes(request):
    """Vista para generar reporte de clientes"""
    return generar_reporte_clientes_csv(request)

def reporte_servicios(request):
    """Vista para generar reporte de servicios"""
    return generar_reporte_servicios_csv(request)

def reporte_compras(request):
    """Vista para generar reporte de compras"""
    return generar_reporte_compras_csv(request)


# ========== MÓDULO DE AYUDA ========== #
def ayuda_centro(request):
    """Centro de ayuda y soporte"""
    context = {
        'titulo': 'Centro de Ayuda'
    }
    return render(request, 'administrador/ayuda_centro.html', context)

def ayuda_faq(request):
    """Preguntas frecuentes"""
    faqs = [
        {
            'categoria': 'Productos',
            'preguntas': [
                {
                    'pregunta': '¿Cómo registro un nuevo producto?',
                    'respuesta': 'Ve a Gestión de Productos, haz clic en "Nuevo Registro", completa el formulario con los datos del producto y presiona "Guardar".'
                },
                {
                    'pregunta': '¿Cómo actualizo el stock de un producto?',
                    'respuesta': 'En la lista de productos, haz clic en el ícono de editar, modifica el campo "Stock Actual" y guarda los cambios.'
                },
                {
                    'pregunta': '¿Qué significa el estado "Stock Bajo"?',
                    'respuesta': 'Un producto tiene stock bajo cuando la cantidad actual es menor o igual al stock mínimo configurado.'
                }
            ]
        },
        {
            'categoria': 'Clientes',
            'preguntas': [
                {
                    'pregunta': '¿Cómo registro un nuevo cliente?',
                    'respuesta': 'Accede a Gestión de Clientes, haz clic en "Nuevo Registro", completa el formulario y guarda.'
                },
                {
                    'pregunta': '¿Cuál es la diferencia entre Persona Natural y Jurídica?',
                    'respuesta': 'Persona Natural es un cliente individual. Persona Jurídica es una empresa u organización.'
                }
            ]
        },
        {
            'categoria': 'Ventas y Facturación',
            'preguntas': [
                {
                    'pregunta': '¿Cómo genero una venta?',
                    'respuesta': 'Ve a Gestión de Ventas, selecciona el cliente, agrega los productos, verifica el total y confirma la venta.'
                },
                {
                    'pregunta': '¿Puedo cancelar una venta?',
                    'respuesta': 'Sí, desde el detalle de la venta puedes cambiar el estado a "Anulada" si tienes los permisos necesarios.'
                }
            ]
        },
        {
            'categoria': 'Servicios Técnicos',
            'preguntas': [
                {
                    'pregunta': '¿Cómo registro una orden de servicio?',
                    'respuesta': 'En Órdenes de Servicio, crea una nueva orden, selecciona el cliente, equipo, describe el problema y asigna un técnico.'
                },
                {
                    'pregunta': '¿Cómo cambio el estado de una orden?',
                    'respuesta': 'Edita la orden y actualiza el campo "Estado" según el avance del servicio.'
                }
            ]
        },
        {
            'categoria': 'Reportes',
            'preguntas': [
                {
                    'pregunta': '¿Cómo genero un reporte de ventas?',
                    'respuesta': 'Ve al Centro de Reportes y haz clic en "Reporte de Ventas". Se descargará un archivo Excel con toda la información.'
                },
                {
                    'pregunta': '¿Qué formato tienen los reportes?',
                    'respuesta': 'Los reportes se generan en formato CSV/Excel, compatible con Microsoft Excel, Google Sheets y LibreOffice.'
                }
            ]
        },
        {
            'categoria': 'Sistema',
            'preguntas': [
                {
                    'pregunta': '¿Cómo cambio mi contraseña?',
                    'respuesta': 'Ve a tu perfil de usuario, haz clic en "Cambiar Contraseña" e ingresa tu contraseña actual y la nueva.'
                },
                {
                    'pregunta': '¿Qué hago si olvidé mi contraseña?',
                    'respuesta': 'En la pantalla de login, haz clic en "¿Olvidaste tu contraseña?" e ingresa tu correo para recibir instrucciones.'
                }
            ]
        }
    ]

    context = {
        'faqs': faqs,
        'titulo': 'Preguntas Frecuentes'
    }
    return render(request, 'administrador/ayuda_faq.html', context)


# ========== MÓDULO DE BACKUP ========== #
from django.core.management import call_command
from django.http import FileResponse
import os
import json

def backup_database(request):
    """Genera un backup de la base de datos"""
    if request.method == 'POST':
        try:
            from django.conf import settings
            import sqlite3
            import shutil
            from datetime import datetime

            # Nombre del archivo de backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'backup_digitsoft_{timestamp}.db'
            backup_path = os.path.join(settings.BASE_DIR, 'backups', backup_filename)

            # Crear directorio de backups si no existe
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            # Copiar la base de datos
            db_path = settings.DATABASES['default']['NAME']
            shutil.copy2(db_path, backup_path)

            messages.success(request, f'Backup creado exitosamente: {backup_filename}')

            # Retornar el archivo para descarga
            return FileResponse(
                open(backup_path, 'rb'),
                as_attachment=True,
                filename=backup_filename
            )
        except Exception as e:
            messages.error(request, f'Error al crear el backup: {str(e)}')

    context = {
        'titulo': 'Backup de Base de Datos'
    }
    return render(request, 'administrador/backup_database.html', context)

def backup_list(request):
    """Lista todos los backups disponibles"""
    from django.conf import settings
    from datetime import datetime

    backups_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []

    if os.path.exists(backups_dir):
        for filename in os.listdir(backups_dir):
            if filename.endswith('.db'):
                filepath = os.path.join(backups_dir, filename)
                backups.append({
                    'nombre': filename,
                    'tamano': os.path.getsize(filepath),
                    'fecha': datetime.fromtimestamp(os.path.getmtime(filepath))
                })

    backups.sort(key=lambda x: x['fecha'], reverse=True)

    context = {
        'backups': backups,
        'titulo': 'Gestión de Backups'
    }
    return render(request, 'administrador/backup_list.html', context)


# ========== E-COMMERCE - TIENDA ONLINE ========== #
from .ecommerce import (
    calcular_totales_carrito,
    verificar_stock_disponible,
    reducir_stock_producto,
    generar_numero_venta,
    generar_numero_factura,
    generar_numero_garantia
)
from datetime import timedelta

def tienda_publica(request):
    """Tienda pública accesible para todos los usuarios"""
    # Obtener parámetros de búsqueda y filtros
    busqueda = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    marca_id = request.GET.get('marca', '')

    # Filtrar productos activos y con stock
    productos = Producto.objects.filter(activo=True).select_related('marca')

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(codigo_producto__icontains=busqueda)
        )

    if categoria:
        productos = productos.filter(categoria=categoria)

    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    # Obtener categorías y marcas para filtros
    categorias = Producto.CATEGORIA_CHOICES
    marcas = Marca.objects.filter(activa=True)

    context = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas,
        'busqueda': busqueda,
        'categoria_actual': categoria,
        'titulo': 'Tienda Online - Digit Soft'
    }
    return render(request, 'administrador/tienda_publica.html', context)

def producto_detalle_tienda(request, producto_id):
    """Vista detallada de un producto en la tienda"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        activo=True
    ).exclude(id=producto_id)[:4]

    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'titulo': f'{producto.nombre} - Digit Soft'
    }
    return render(request, 'administrador/producto_detalle_tienda.html', context)

def agregar_al_carrito(request, producto_id):
    """Agregar producto al carrito"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        cantidad = int(request.POST.get('cantidad', 1))

        # Verificar stock
        if not verificar_stock_disponible(producto, cantidad):
            messages.error(request, f'No hay suficiente stock disponible. Stock actual: {producto.stock_actual}')
            return redirect('administrador:producto_detalle_tienda', producto_id=producto_id)

        # Obtener o crear carrito del usuario
        if request.user.is_authenticated:
            try:
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                messages.error(request, 'Debes tener un perfil de cliente para comprar.')
                return redirect('administrador:tienda_publica')

            carrito, created = Carrito.objects.get_or_create(
                cliente=cliente,
                estado='ACTIVO'
            )
        else:
            messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')
            return redirect('autenticacion:login')

        # Agregar o actualizar item en el carrito
        from administrador.models import ItemCarrito
        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad, 'precio_unitario': producto.precio_venta}
        )

        if not created:
            item.cantidad += cantidad
            item.save()

        carrito.actualizar_totales()
        messages.success(request, f'{producto.nombre} agregado al carrito correctamente.')
        return redirect('administrador:ver_carrito')

    return redirect('administrador:tienda_publica')

def ver_carrito(request):
    """Ver el carrito de compras del usuario"""
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para ver tu carrito.')
        return redirect('autenticacion:login')

    try:
        cliente = Cliente.objects.get(user=request.user)
        carrito = Carrito.objects.get(cliente=cliente, estado='ACTIVO')
        items = carrito.items.all()
        totales = calcular_totales_carrito(items)
    except (Cliente.DoesNotExist, Carrito.DoesNotExist):
        items = []
        totales = {'subtotal': 0, 'iva': 0, 'total': 0, 'cantidad_items': 0}
        carrito = None

    context = {
        'carrito': carrito,
        'items': items,
        'totales': totales,
        'titulo': 'Mi Carrito'
    }
    return render(request, 'administrador/ver_carrito.html', context)

def procesar_compra(request):
    """Procesar la compra y generar venta, factura y garantía"""
    if request.method != 'POST':
        return redirect('administrador:ver_carrito')

    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para realizar la compra.')
        return redirect('autenticacion:login')

    try:
        cliente = Cliente.objects.get(user=request.user)
        carrito = Carrito.objects.get(cliente=cliente, estado='ACTIVO')
        items = carrito.items.all()

        if not items.exists():
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('administrador:ver_carrito')

        # Verificar stock de todos los productos
        for item in items:
            if not verificar_stock_disponible(item.producto, item.cantidad):
                messages.error(request, f'No hay suficiente stock de {item.producto.nombre}')
                return redirect('administrador:ver_carrito')

        # Calcular totales
        totales = calcular_totales_carrito(items)
        metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')

        # 1. CREAR VENTA
        venta = Venta.objects.create(
            numero_venta=generar_numero_venta(),
            cliente=cliente,
            vendedor=None,  # Venta online
            subtotal=totales['subtotal'],
            descuento=Decimal('0.00'),
            impuestos=totales['iva'],
            total=totales['total'],
            metodo_pago=metodo_pago,
            estado='PAGADA' if metodo_pago != 'CREDITO' else 'CREDITO'
        )

        # 2. CREAR DETALLES DE VENTA Y REDUCIR STOCK
        for item in items:
            # Crear detalle de venta (si tienes el modelo DetalleVenta)
            # DetalleVenta.objects.create(...)

            # Reducir stock
            reducir_stock_producto(item.producto, item.cantidad)

        # 3. CREAR FACTURA
        factura = Factura.objects.create(
            numero_factura=generar_numero_factura(),
            cliente=cliente,
            venta=venta,
            tipo_factura='VENTA',
            estado='EMITIDA',
            subtotal=totales['subtotal'],
            descuento=Decimal('0.00'),
            impuestos=totales['iva'],
            total=totales['total'],
            fecha_vencimiento=(timezone.now() + timedelta(days=30)).date()
        )

        # 4. CREAR GARANTÍAS PARA CADA PRODUCTO
        garantias_creadas = []
        for item in items:
            if item.producto.garantia_meses > 0:
                garantia = Garantia.objects.create(
                    numero_garantia=generar_numero_garantia(),
                    producto=item.producto,
                    cliente=cliente,
                    venta=venta,
                    tipo_garantia='FABRICANTE',
                    fecha_inicio=timezone.now().date(),
                    fecha_vencimiento=(timezone.now() + timedelta(days=item.producto.garantia_meses * 30)).date(),
                    duracion_meses=item.producto.garantia_meses,
                    estado='VIGENTE',
                    condiciones=f'Garantía del fabricante para {item.producto.nombre}',
                    cobertura='Defectos de fabricación',
                    exclusiones='Daños por mal uso o accidentes'
                )
                garantias_creadas.append(garantia)

        # 5. MARCAR CARRITO COMO CONVERTIDO
        carrito.estado = 'CONVERTIDO'
        carrito.venta_generada = venta
        carrito.save()

        messages.success(request, '¡Compra realizada exitosamente!')
        return redirect('administrador:compra_exitosa', venta_id=venta.id)

    except Exception as e:
        messages.error(request, f'Error al procesar la compra: {str(e)}')
        return redirect('administrador:ver_carrito')

def compra_exitosa(request, venta_id):
    """Página de confirmación de compra con factura y garantías"""
    venta = get_object_or_404(Venta, id=venta_id)

    # Verificar que la venta pertenece al usuario actual
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(user=request.user)
            if venta.cliente != cliente:
                messages.error(request, 'No tienes permiso para ver esta compra.')
                return redirect('administrador:tienda_publica')
        except Cliente.DoesNotExist:
            messages.error(request, 'Perfil de cliente no encontrado.')
            return redirect('administrador:tienda_publica')

    factura = Factura.objects.filter(venta=venta).first()
    garantias = Garantia.objects.filter(venta=venta)

    context = {
        'venta': venta,
        'factura': factura,
        'garantias': garantias,
        'titulo': 'Compra Exitosa'
    }
    return render(request, 'administrador/compra_exitosa.html', context)

def mis_compras(request):
    """Lista de compras del usuario"""
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión.')
        return redirect('autenticacion:login')

    try:
        cliente = Cliente.objects.get(user=request.user)
        ventas = Venta.objects.filter(cliente=cliente).order_by('-fecha_venta')

        # Calcular total gastado
        from django.db.models import Sum
        total_gastado = ventas.aggregate(total=Sum('total'))['total'] or 0

    except Cliente.DoesNotExist:
        ventas = []
        total_gastado = 0

    context = {
        'ventas': ventas,
        'total_gastado': total_gastado,
        'titulo': 'Mis Compras'
    }
    return render(request, 'administrador/mis_compras.html', context)

def mis_garantias(request):
    """Lista de garantías del usuario"""
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión.')
        return redirect('autenticacion:login')

    try:
        cliente = Cliente.objects.get(user=request.user)
        garantias = Garantia.objects.filter(cliente=cliente).order_by('-fecha_inicio')
    except Cliente.DoesNotExist:
        garantias = []

    context = {
        'garantias': garantias,
        'titulo': 'Mis Garantías'
    }
    return render(request, 'administrador/mis_garantias.html', context)
