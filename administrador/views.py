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
    context = {
        'compras': compras,
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
    garantias = Garantia.objects.select_related('producto', 'cliente').all()
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
