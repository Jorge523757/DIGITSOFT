"""
DigitSoft - Módulo de Administrador
Views

Define las vistas para la gestión administrativa.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from autenticacion.decorators import admin_required


# ========== VISTA PRINCIPAL DEL PANEL DE ADMINISTRACIÓN ========== #
@login_required
@admin_required
def dashboard(request):
    """
    Vista principal del panel de administración.
    Muestra un resumen general del sistema.
    """
    context = {
        'titulo': 'Panel de Administración',
        'seccion': 'dashboard'
    }
    return render(request, 'administrador/dashboard.html', context)


# ========== GESTIÓN DE CONFIGURACIÓN ========== #
@login_required
@admin_required
def configuracion(request):
    """
    Vista para gestionar la configuración general del sistema.
    """
    from .models import ConfiguracionGeneral

    config = ConfiguracionGeneral.objects.filter(activa=True).first()

    context = {
        'titulo': 'Configuración General',
        'seccion': 'configuracion',
        'config': config
    }
    return render(request, 'administrador/configuracion.html', context)


# ========== GESTIÓN DE LOGS ========== #
@login_required
@admin_required
def logs_actividad(request):
    """
    Vista para ver los logs de actividad del sistema.
    """
    from .models import LogActividad

    logs = LogActividad.objects.all().select_related('administrador', 'administrador__user')[:100]

    context = {
        'titulo': 'Logs de Actividad',
        'seccion': 'logs',
        'logs': logs
    }
    return render(request, 'administrador/logs.html', context)


# ========================================================================
# GESTIÓN DE PRODUCTOS
# ========================================================================
@login_required
@admin_required
def producto_list(request):
    """Vista para listar productos"""
    from .models import Producto
    productos = Producto.objects.all()
    context = {
        'titulo': 'Gestión de Productos',
        'seccion': 'productos',
        'productos': productos
    }
    return render(request, 'administrador/producto_list.html', context)


@login_required
@admin_required
def producto_create(request):
    """Vista para crear producto"""
    from .forms import ProductoForm
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('administrador:producto_list')
    else:
        form = ProductoForm()

    context = {'titulo': 'Crear Producto', 'form': form}
    return render(request, 'administrador/producto_form.html', context)


@login_required
@admin_required
def producto_update(request, pk):
    """Vista para actualizar producto"""
    from .models import Producto
    from .forms import ProductoForm
    from django.shortcuts import get_object_or_404

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('administrador:producto_list')
    else:
        form = ProductoForm(instance=producto)

    context = {'titulo': 'Editar Producto', 'form': form, 'producto': producto}
    return render(request, 'administrador/producto_form.html', context)


@login_required
@admin_required
def producto_delete(request, pk):
    """Vista para eliminar producto"""
    from .models import Producto
    from django.shortcuts import get_object_or_404

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('administrador:producto_list')

    context = {'titulo': 'Eliminar Producto', 'producto': producto}
    return render(request, 'administrador/producto_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE COMPRAS
# ========================================================================
@login_required
@admin_required
def compra_list(request):
    """Vista para listar compras"""
    context = {'titulo': 'Gestión de Compras', 'seccion': 'compras'}
    return render(request, 'administrador/compra_list.html', context)


@login_required
@admin_required
def compra_create(request):
    """Vista para crear compra"""
    context = {'titulo': 'Nueva Compra'}
    return render(request, 'administrador/compra_form.html', context)


@login_required
@admin_required
def compra_detail(request, pk):
    """Vista para detalle de compra"""
    context = {'titulo': 'Detalle de Compra', 'compra_id': pk}
    return render(request, 'administrador/compra_detail.html', context)


# ========================================================================
# GESTIÓN DE VENTAS
# ========================================================================
@login_required
@admin_required
def venta_list(request):
    """Vista para listar ventas"""
    context = {'titulo': 'Gestión de Ventas', 'seccion': 'ventas'}
    return render(request, 'administrador/venta_list.html', context)


@login_required
@admin_required
def venta_create(request):
    """Vista para crear venta"""
    context = {'titulo': 'Nueva Venta'}
    return render(request, 'administrador/venta_form.html', context)


@login_required
@admin_required
def venta_detail(request, pk):
    """Vista para detalle de venta"""
    context = {'titulo': 'Detalle de Venta', 'venta_id': pk}
    return render(request, 'administrador/venta_detail.html', context)


# ========================================================================
# GESTIÓN DE CLIENTES
# ========================================================================
@login_required
@admin_required
def cliente_list(request):
    """Vista para listar clientes"""
    from .models import Cliente
    clientes = Cliente.objects.all()
    context = {'titulo': 'Gestión de Clientes', 'seccion': 'clientes', 'clientes': clientes}
    return render(request, 'administrador/cliente_list.html', context)


@login_required
@admin_required
def cliente_create(request):
    """Vista para crear cliente"""
    context = {'titulo': 'Nuevo Cliente'}
    return render(request, 'administrador/cliente_form.html', context)


@login_required
@admin_required
def cliente_update(request, pk):
    """Vista para actualizar cliente"""
    context = {'titulo': 'Editar Cliente', 'cliente_id': pk}
    return render(request, 'administrador/cliente_form.html', context)


@login_required
@admin_required
def cliente_delete(request, pk):
    """Vista para eliminar cliente"""
    context = {'titulo': 'Eliminar Cliente', 'cliente_id': pk}
    return render(request, 'administrador/cliente_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE EQUIPOS
# ========================================================================
@login_required
@admin_required
def equipo_list(request):
    """Vista para listar equipos"""
    from .models import Equipo
    equipos = Equipo.objects.all()
    context = {'titulo': 'Gestión de Equipos', 'seccion': 'equipos', 'equipos': equipos}
    return render(request, 'administrador/equipo_list.html', context)


@login_required
@admin_required
def equipo_create(request):
    """Vista para crear equipo"""
    context = {'titulo': 'Nuevo Equipo'}
    return render(request, 'administrador/equipo_form.html', context)


@login_required
@admin_required
def equipo_update(request, pk):
    """Vista para actualizar equipo"""
    context = {'titulo': 'Editar Equipo', 'equipo_id': pk}
    return render(request, 'administrador/equipo_form.html', context)


@login_required
@admin_required
def equipo_delete(request, pk):
    """Vista para eliminar equipo"""
    context = {'titulo': 'Eliminar Equipo', 'equipo_id': pk}
    return render(request, 'administrador/equipo_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE FACTURACIÓN
# ========================================================================
@login_required
@admin_required
def facturacion_list(request):
    """Vista para listar facturas"""
    context = {'titulo': 'Gestión de Facturación', 'seccion': 'facturacion'}
    return render(request, 'administrador/facturacion_list.html', context)


@login_required
@admin_required
def facturacion_create(request):
    """Vista para crear factura"""
    context = {'titulo': 'Nueva Factura'}
    return render(request, 'administrador/facturacion_form.html', context)


@login_required
@admin_required
def facturacion_detail(request, pk):
    """Vista para detalle de factura"""
    context = {'titulo': 'Detalle de Factura', 'factura_id': pk}
    return render(request, 'administrador/facturacion_detail.html', context)


@login_required
@admin_required
def facturacion_pdf(request, pk):
    """Vista para generar PDF de factura"""
    from django.http import HttpResponse
    return HttpResponse("Generación de PDF en desarrollo", content_type="application/pdf")


# ========================================================================
# GESTIÓN DE GARANTÍAS
# ========================================================================
@login_required
@admin_required
def garantia_list(request):
    """Vista para listar garantías"""
    from .models import Garantia
    garantias = Garantia.objects.all()
    context = {'titulo': 'Gestión de Garantías', 'seccion': 'garantias', 'garantias': garantias}
    return render(request, 'administrador/garantia_list.html', context)


@login_required
@admin_required
def garantia_create(request):
    """Vista para crear garantía"""
    context = {'titulo': 'Nueva Garantía'}
    return render(request, 'administrador/garantia_form.html', context)


@login_required
@admin_required
def garantia_detail(request, pk):
    """Vista para detalle de garantía"""
    context = {'titulo': 'Detalle de Garantía', 'garantia_id': pk}
    return render(request, 'administrador/garantia_detail.html', context)


@login_required
def mis_garantias(request):
    """Vista para que clientes vean sus garantías"""
    context = {'titulo': 'Mis Garantías', 'seccion': 'mis_garantias'}
    return render(request, 'administrador/mis_garantias.html', context)


# ========================================================================
# GESTIÓN DE MARCAS
# ========================================================================
@login_required
@admin_required
def marca_list(request):
    """Vista para listar marcas"""
    from .models import Marca
    marcas = Marca.objects.all()
    context = {'titulo': 'Gestión de Marcas', 'seccion': 'marcas', 'marcas': marcas}
    return render(request, 'administrador/marca_list.html', context)


@login_required
@admin_required
def marca_create(request):
    """Vista para crear marca"""
    context = {'titulo': 'Nueva Marca'}
    return render(request, 'administrador/marca_form.html', context)


@login_required
@admin_required
def marca_update(request, pk):
    """Vista para actualizar marca"""
    context = {'titulo': 'Editar Marca', 'marca_id': pk}
    return render(request, 'administrador/marca_form.html', context)


@login_required
@admin_required
def marca_delete(request, pk):
    """Vista para eliminar marca"""
    context = {'titulo': 'Eliminar Marca', 'marca_id': pk}
    return render(request, 'administrador/marca_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE PROVEEDORES
# ========================================================================
@login_required
@admin_required
def proveedor_list(request):
    """Vista para listar proveedores"""
    from .models import Proveedor
    proveedores = Proveedor.objects.all()
    context = {'titulo': 'Gestión de Proveedores', 'seccion': 'proveedores', 'proveedores': proveedores}
    return render(request, 'administrador/proveedor_list.html', context)


@login_required
@admin_required
def proveedor_create(request):
    """Vista para crear proveedor"""
    context = {'titulo': 'Nuevo Proveedor'}
    return render(request, 'administrador/proveedor_form.html', context)


@login_required
@admin_required
def proveedor_update(request, pk):
    """Vista para actualizar proveedor"""
    context = {'titulo': 'Editar Proveedor', 'proveedor_id': pk}
    return render(request, 'administrador/proveedor_form.html', context)


@login_required
@admin_required
def proveedor_delete(request, pk):
    """Vista para eliminar proveedor"""
    context = {'titulo': 'Eliminar Proveedor', 'proveedor_id': pk}
    return render(request, 'administrador/proveedor_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE TÉCNICOS
# ========================================================================
@login_required
@admin_required
def tecnico_list(request):
    """Vista para listar técnicos"""
    from .models import Tecnico
    tecnicos = Tecnico.objects.all()
    context = {'titulo': 'Gestión de Técnicos', 'seccion': 'tecnicos', 'tecnicos': tecnicos}
    return render(request, 'administrador/tecnico_list.html', context)


@login_required
@admin_required
def tecnico_create(request):
    """Vista para crear técnico"""
    context = {'titulo': 'Nuevo Técnico'}
    return render(request, 'administrador/tecnico_form.html', context)


@login_required
@admin_required
def tecnico_update(request, pk):
    """Vista para actualizar técnico"""
    context = {'titulo': 'Editar Técnico', 'tecnico_id': pk}
    return render(request, 'administrador/tecnico_form.html', context)


@login_required
@admin_required
def tecnico_delete(request, pk):
    """Vista para eliminar técnico"""
    context = {'titulo': 'Eliminar Técnico', 'tecnico_id': pk}
    return render(request, 'administrador/tecnico_confirm_delete.html', context)


# ========================================================================
# GESTIÓN DE TIENDA ONLINE
# ========================================================================
@login_required
@admin_required
def tienda_list(request):
    """Vista para administrar la tienda online"""
    context = {'titulo': 'Administración de Tienda', 'seccion': 'tienda'}
    return render(request, 'administrador/tienda_list.html', context)


@login_required
@admin_required
def tienda_config(request):
    """Vista para configurar la tienda"""
    context = {'titulo': 'Configuración de Tienda'}
    return render(request, 'administrador/tienda_config.html', context)


# ========================================================================
# GESTIÓN DE ÓRDENES DE SERVICIO
# ========================================================================
@login_required
def orden_servicio_list(request):
    """Vista para listar órdenes de servicio"""
    context = {'titulo': 'Órdenes de Servicio', 'seccion': 'ordenes'}
    return render(request, 'administrador/orden_servicio_list.html', context)


@login_required
def orden_servicio_create(request):
    """Vista para crear orden de servicio"""
    context = {'titulo': 'Nueva Orden de Servicio'}
    return render(request, 'administrador/orden_servicio_form.html', context)


@login_required
def orden_servicio_detail(request, pk):
    """Vista para detalle de orden de servicio"""
    context = {'titulo': 'Detalle de Orden', 'orden_id': pk}
    return render(request, 'administrador/orden_servicio_detail.html', context)


@login_required
def orden_servicio_update(request, pk):
    """Vista para actualizar orden de servicio"""
    context = {'titulo': 'Editar Orden de Servicio', 'orden_id': pk}
    return render(request, 'administrador/orden_servicio_form.html', context)


# ========================================================================
# GESTIÓN DE SERVICIOS TÉCNICOS
# ========================================================================
@login_required
def servicio_tecnico_list(request):
    """Vista para listar servicios técnicos"""
    context = {'titulo': 'Servicios Técnicos', 'seccion': 'servicios'}
    return render(request, 'administrador/servicio_tecnico_list.html', context)


@login_required
def servicio_tecnico_create(request):
    """Vista para crear servicio técnico"""
    context = {'titulo': 'Nuevo Servicio Técnico'}
    return render(request, 'administrador/servicio_tecnico_form.html', context)


@login_required
def servicio_tecnico_detail(request, pk):
    """Vista para detalle de servicio técnico"""
    context = {'titulo': 'Detalle de Servicio', 'servicio_id': pk}
    return render(request, 'administrador/servicio_tecnico_detail.html', context)


# ========================================================================
# GESTIÓN DE CARRITOS
# ========================================================================
@login_required
@admin_required
def carrito_list(request):
    """Vista para listar carritos"""
    context = {'titulo': 'Gestión de Carritos', 'seccion': 'carritos'}
    return render(request, 'administrador/carrito_list.html', context)


@login_required
@admin_required
def carrito_detail(request, pk):
    """Vista para detalle de carrito"""
    context = {'titulo': 'Detalle de Carrito', 'carrito_id': pk}
    return render(request, 'administrador/carrito_detail.html', context)


# ========================================================================
# MÓDULOS DE AYUDA
# ========================================================================
@login_required
def ayuda_faq(request):
    """Vista para preguntas frecuentes"""
    context = {'titulo': 'Preguntas Frecuentes', 'seccion': 'ayuda'}
    return render(request, 'administrador/ayuda_faq.html', context)


@login_required
def ayuda_manual(request):
    """Vista para manual de usuario"""
    context = {'titulo': 'Manual de Usuario'}
    return render(request, 'administrador/ayuda_manual.html', context)


# ========================================================================
# MÓDULOS DE BACKUP
# ========================================================================
@login_required
@admin_required
def backup_database(request):
    """Vista para realizar backup de la base de datos"""
    context = {'titulo': 'Backup de Base de Datos', 'seccion': 'backup'}
    return render(request, 'administrador/backup_database.html', context)


@login_required
@admin_required
def backup_restore(request):
    """Vista para restaurar backup"""
    context = {'titulo': 'Restaurar Backup'}
    return render(request, 'administrador/backup_restore.html', context)
