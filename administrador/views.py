from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import F
from django.utils import timezone
from .models import (
    Cliente, Tecnico, Marca, Proveedor, Producto,
    Equipo, ServicioTecnico, OrdenServicio, Compra, Carrito,
    Venta, Garantia, Factura, LogActividad, ConfiguracionGeneral
)
from .forms import (
    ProveedorForm
)

# ========== DASHBOARD ========== #
def dashboard(request):
    """Vista principal del dashboard del administrador"""
    # Estadísticas generales
    stats = {
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_productos': Producto.objects.filter(activo=True).count(),
        'ordenes_pendientes': OrdenServicio.objects.filter(estado='PENDIENTE').count(),
        'ventas_mes': Venta.objects.filter(fecha_venta__month=timezone.now().month).count(),
        'equipos_reparacion': Equipo.objects.filter(estado_fisico='EN_REPARACION').count(),
        'tecnicos_disponibles': Tecnico.objects.filter(estado_actual='DISPONIBLE').count(),
    }

    # Órdenes recientes
    ordenes_recientes = OrdenServicio.objects.select_related('cliente', 'tecnico_asignado')[:5]

    # Productos con stock bajo
    productos_stock_bajo = Producto.objects.filter(
        stock_actual__lte=F('stock_minimo')
    )[:5]

    context = {
        'stats': stats,
        'ordenes_recientes': ordenes_recientes,
        'productos_stock_bajo': productos_stock_bajo,
        'titulo': 'Dashboard - DigitSoft'
    }
    return render(request, 'administrador/dashboard.html', context)

# ========== CLIENTES ========== #
def cliente_list(request):
    """Vista para listar clientes"""
    clientes = Cliente.objects.filter(activo=True)
    context = {
        'clientes': clientes,
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

# ========== PRODUCTOS ========== #
def producto_list(request):
    """Vista para listar productos"""
    productos = Producto.objects.select_related('marca', 'proveedor_principal').filter(activo=True)
    context = {
        'productos': productos,
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

# ========== EQUIPOS ========== #
def equipo_list(request):
    """Vista para listar equipos"""
    if request.method == 'POST':
        try:
            equipo_id = request.POST.get('equipo_id')

            # Datos del formulario
            codigo_equipo = request.POST.get('codigo_equipo')
            nombre = request.POST.get('nombre')
            cliente_id = request.POST.get('cliente')
            tipo_equipo = request.POST.get('tipo_equipo')
            marca_id = request.POST.get('marca')
            modelo = request.POST.get('modelo')
            serial = request.POST.get('serial')
            estado_fisico = request.POST.get('estado_fisico')
            especificaciones = request.POST.get('especificaciones', '')

            # Obtener objetos relacionados
            cliente = get_object_or_404(Cliente, id=cliente_id)
            marca = get_object_or_404(Marca, id=marca_id)

            if equipo_id:  # Editar equipo existente
                equipo = get_object_or_404(Equipo, id=equipo_id)
                equipo.codigo_equipo = codigo_equipo
                equipo.nombre = nombre
                equipo.cliente = cliente
                equipo.tipo_equipo = tipo_equipo
                equipo.marca = marca
                equipo.modelo = modelo
                equipo.serial = serial
                equipo.estado_fisico = estado_fisico
                equipo.especificaciones = especificaciones
                equipo.save()
                messages.success(request, f'Equipo {equipo.codigo_equipo} actualizado correctamente.')
            else:  # Crear nuevo equipo
                equipo = Equipo.objects.create(
                    codigo_equipo=codigo_equipo,
                    nombre=nombre,
                    cliente=cliente,
                    tipo_equipo=tipo_equipo,
                    marca=marca,
                    modelo=modelo,
                    serial=serial,
                    estado_fisico=estado_fisico,
                    especificaciones=especificaciones
                )
                messages.success(request, f'Equipo {equipo.codigo_equipo} registrado correctamente.')

        except Exception as e:
            messages.error(request, f'Error al guardar el equipo: {str(e)}')

        return redirect('administrador:equipo_list')

    # GET request - mostrar lista
    equipos = Equipo.objects.select_related('cliente', 'marca').filter(activo=True)
    clientes = Cliente.objects.filter(activo=True).order_by('nombres', 'apellidos')
    marcas = Marca.objects.filter(activa=True).order_by('nombre')

    context = {
        'equipos': equipos,
        'clientes': clientes,
        'marcas': marcas,
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

# ========== TÉCNICOS ========== #
def tecnico_list(request):
    """Vista para listar técnicos"""
    tecnicos = Tecnico.objects.filter(activo=True).order_by('apellidos', 'nombres')

    context = {
        'tecnicos': tecnicos,
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

# ========== MARCAS ========== #
def marca_list(request):
    """Vista para listar marcas"""
    marcas = Marca.objects.filter(activa=True)
    context = {
        'marcas': marcas,
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

# ========== PROVEEDORES ========== #
def proveedor_list(request):
    """Vista para listar proveedores"""
    form = ProveedorForm()

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')

        if proveedor_id:  # Editar proveedor existente
            proveedor = get_object_or_404(Proveedor, id=proveedor_id)
            form = ProveedorForm(request.POST, instance=proveedor)
        else:  # Crear nuevo proveedor
            form = ProveedorForm(request.POST)

        if form.is_valid():
            proveedor = form.save()
            if proveedor_id:
                messages.success(request, f'✅ Proveedor "{proveedor.razon_social}" actualizado correctamente.')
            else:
                messages.success(request, f'✅ Proveedor "{proveedor.razon_social}" registrado correctamente.')
            return redirect('administrador:proveedor_list')
        else:
            # Si hay errores, se mostrarán en el template
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label if field in form.fields else field
                    messages.error(request, f'❌ Error en {field_label}: {error}')

    # GET request - mostrar lista
    proveedores = Proveedor.objects.filter(activo=True).order_by('razon_social')

    context = {
        'proveedores': proveedores,
        'form': form,
        'titulo': 'Gestión de Proveedores'
    }
    return render(request, 'administrador/proveedor_list.html', context)

def proveedor_detail(request, proveedor_id):
    """Vista de detalle de proveedor"""
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    productos_proveedor = Producto.objects.filter(proveedor_principal=proveedor)
    compras_proveedor = Compra.objects.filter(proveedor=proveedor)[:10]
    context = {
        'proveedor': proveedor,
        'productos_proveedor': productos_proveedor,
        'compras_proveedor': compras_proveedor,
        'titulo': f'Proveedor: {proveedor.razon_social}'
    }
    return render(request, 'administrador/proveedor_detail.html', context)

# ========== ÓRDENES DE SERVICIO ========== #
def orden_servicio_list(request):
    """Vista para listar órdenes de servicio"""
    ordenes = OrdenServicio.objects.select_related('cliente', 'equipo', 'tecnico_asignado')
    context = {
        'ordenes': ordenes,
        'titulo': 'Órdenes de Servicio'
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

# ========== SERVICIOS TÉCNICOS ========== #
def servicio_tecnico_list(request):
    """Vista para listar servicios técnicos"""
    servicios = ServicioTecnico.objects.filter(activo=True)
    context = {
        'servicios': servicios,
        'titulo': 'Servicios Técnicos'
    }
    return render(request, 'administrador/servicio_tecnico_list.html', context)

def servicio_tecnico_detail(request, servicio_id):
    """Vista de detalle de servicio técnico"""
    servicio = get_object_or_404(ServicioTecnico, id=servicio_id)
    context = {
        'servicio': servicio,
        'titulo': f'Servicio: {servicio.nombre}'
    }
    return render(request, 'administrador/servicio_tecnico_detail.html', context)

# ========== COMPRAS ========== #
def compra_list(request):
    """Vista para listar y crear compras"""
    if request.method == 'POST':
        # Crear nueva compra
        try:
            # Obtener proveedor
            proveedor = get_object_or_404(Proveedor, id=request.POST.get('proveedor'))

            # Crear la compra
            compra = Compra.objects.create(
                numero_compra=request.POST.get('numero_compra'),
                proveedor=proveedor,
                fecha_solicitud=request.POST.get('fecha_solicitud'),
                estado=request.POST.get('estado', 'SOLICITUD'),
                subtotal=request.POST.get('subtotal', 0),
                impuestos=request.POST.get('impuestos', 0),
                total=request.POST.get('total', 0),
                metodo_pago=request.POST.get('metodo_pago') or None,
                observaciones=request.POST.get('observaciones', '')
            )

            messages.success(request, f'Compra {compra.numero_compra} creada exitosamente')
            return redirect('administrador:compra_list')

        except Exception as e:
            messages.error(request, f'Error al crear la compra: {str(e)}')

    # Listar compras
    compras = Compra.objects.select_related('proveedor', 'solicitado_por').order_by('-fecha_solicitud')
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
    carritos = Carrito.objects.select_related('cliente')
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

# ========== VENTAS ========== #
def venta_list(request):
    """Vista para listar ventas"""
    ventas = Venta.objects.select_related('cliente', 'vendedor')
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

# ========== FACTURACIÓN ========== #
def facturacion_list(request):
    """Vista para listar facturas"""
    facturas = Factura.objects.select_related('cliente', 'venta', 'orden_servicio')
    context = {
        'facturas': facturas,
        'titulo': 'Facturación'
    }
    return render(request, 'administrador/facturacion_list.html', context)

def factura_detail(request, factura_id):
    """Vista de detalle de factura"""
    factura = get_object_or_404(Factura, id=factura_id)
    context = {
        'factura': factura,
        'titulo': f'Factura: {factura.numero_factura}'
    }
    return render(request, 'administrador/factura_detail.html', context)

# ========== GARANTÍAS ========== #
def garantia_list(request):
    """Vista para listar garantías"""
    garantias = Garantia.objects.select_related('cliente', 'producto', 'equipo')
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

# ========== LOGS Y AUDITORÍA ========== #
def log_actividad_list(request):
    """Vista para listar logs de actividad"""
    logs = LogActividad.objects.select_related('administrador')[:100]
    context = {
        'logs': logs,
        'titulo': 'Logs de Actividad'
    }
    return render(request, 'administrador/log_actividad_list.html', context)

# ========== CONFIGURACIÓN ========== #
def configuracion_general(request):
    """Vista para configuración general del sistema"""
    try:
        config = ConfiguracionGeneral.objects.filter(activa=True).first()
    except ConfiguracionGeneral.DoesNotExist:
        config = None

    context = {
        'config': config,
        'titulo': 'Configuración General'
    }
    return render(request, 'administrador/configuracion_general.html', context)
