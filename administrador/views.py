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
    from inventario.models import Producto
    productos = Producto.objects.all().select_related('marca', 'proveedor_principal').order_by('-fecha_registro')
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
            producto = form.save(commit=False)
            # Manejar el campo activo manualmente
            producto.activo = request.POST.get('activo') == 'on'
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente y listo para la tienda online.')
            return redirect('administrador:producto_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ProductoForm()

    context = {'titulo': 'Crear Producto', 'form': form}
    return render(request, 'administrador/producto_form.html', context)


@login_required
@admin_required
def producto_update(request, pk):
    """Vista para actualizar producto"""
    from inventario.models import Producto
    from .forms import ProductoForm
    from django.shortcuts import get_object_or_404

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            # Manejar el campo activo manualmente
            producto.activo = request.POST.get('activo') == 'on'
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('administrador:producto_list')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ProductoForm(instance=producto)

    context = {'titulo': 'Editar Producto', 'form': form, 'producto': producto}
    return render(request, 'administrador/producto_form.html', context)


@login_required
@admin_required
def producto_delete(request, pk):
    """Vista para eliminar producto"""
    from inventario.models import Producto
    from django.shortcuts import get_object_or_404

    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        # Eliminar imagen si existe
        if producto.imagen:
            producto.imagen.delete()
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
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
    from clientes.models import Cliente
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


def tienda_publica(request):
    """
    Vista pública de la tienda online. Muestra todos los productos activos.
    """
    from inventario.models import Producto

    productos = Producto.objects.filter(activo=True)
    context = {
        'productos': productos,
        'titulo': 'Tienda Online',
        'seccion': 'tienda_publica',
    }
    return render(request, 'administrador/tienda_publica.html', context)


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
# MÓDULOS DE REPORTES
# ========================================================================
@login_required
@admin_required
def reportes_ventas(request):
    """Vista para generar reportes de ventas"""
    from datetime import datetime, timedelta
    from django.db.models import Sum, Count
    from ventas.models import Venta

    # Obtener parámetros de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    ventas = Venta.objects.all()

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=fecha_fin)

    # Estadísticas
    total_ventas = ventas.aggregate(total=Sum('total'))['total'] or 0
    cantidad_ventas = ventas.count()

    context = {
        'titulo': 'Reportes de Ventas',
        'seccion': 'reportes',
        'ventas': ventas[:50],
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'administrador/reportes_ventas.html', context)


@login_required
@admin_required
def reportes_inventario(request):
    """Vista para generar reportes de inventario"""
    from inventario.models import Producto
    from django.db import models

    productos = Producto.objects.all()

    # Productos con bajo stock
    productos_bajo_stock = productos.filter(stock_actual__lte=models.F('stock_minimo'))

    context = {
        'titulo': 'Reportes de Inventario',
        'seccion': 'reportes',
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
        'total_productos': productos.count(),
    }
    return render(request, 'administrador/reportes_inventario.html', context)


@login_required
@admin_required
def reportes_clientes(request):
    """Vista para generar reportes de clientes"""
    from clientes.models import Cliente

    clientes = Cliente.objects.all()

    context = {
        'titulo': 'Reportes de Clientes',
        'seccion': 'reportes',
        'clientes': clientes,
        'total_clientes': clientes.count(),
    }
    return render(request, 'administrador/reportes_clientes.html', context)


@login_required
@admin_required
def generar_pdf_reporte(request):
    """Vista para generar reportes en PDF"""
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from io import BytesIO

    tipo_reporte = request.GET.get('tipo', 'ventas')

    # Crear el PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Reporte de {tipo_reporte.capitalize()}")

    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Contenido básico
    y_position = 680
    p.drawString(100, y_position, "Este es un reporte generado por DigitSoft")

    # Finalizar PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{tipo_reporte}.pdf"'

    return response


# ========================================================================
# MÓDULOS DE AYUDA
# ========================================================================
@login_required
def ayuda_faq(request):
    """Vista para preguntas frecuentes"""
    faqs = [
        {
            'pregunta': '¿Cómo crear un nuevo producto?',
            'respuesta': 'Vaya a Productos > Nuevo Producto y complete el formulario con la información requerida.'
        },
        {
            'pregunta': '¿Cómo gestionar marcas?',
            'respuesta': 'Acceda al módulo de Marcas desde el menú principal para agregar, editar o eliminar marcas.'
        },
        {
            'pregunta': '¿Cómo generar un reporte?',
            'respuesta': 'Vaya a Reportes, seleccione el tipo de reporte y el rango de fechas deseado.'
        },
        {
            'pregunta': '¿Cómo realizar un backup?',
            'respuesta': 'En el módulo de Backup puede crear copias de seguridad de la base de datos.'
        },
    ]

    context = {
        'titulo': 'Preguntas Frecuentes',
        'seccion': 'ayuda',
        'faqs': faqs
    }
    return render(request, 'administrador/ayuda_faq.html', context)


@login_required
def ayuda_manual(request):
    """Vista para manual de usuario"""
    context = {
        'titulo': 'Manual de Usuario',
        'seccion': 'ayuda'
    }
    return render(request, 'administrador/ayuda_manual.html', context)


# ========================================================================
# MÓDULOS DE BACKUP
# ========================================================================
@login_required
@admin_required
def backup_database(request):
    """Vista para realizar backup de la base de datos"""
    import os
    import shutil
    from django.conf import settings
    from datetime import datetime

    if request.method == 'POST':
        try:
            # Ruta de la base de datos actual
            db_path = settings.DATABASES['default']['NAME']

            # Crear carpeta de backups si no existe
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)

            # Nombre del archivo de backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'backup_digitsoft_{timestamp}.db'
            backup_path = os.path.join(backup_dir, backup_filename)

            # Copiar la base de datos
            shutil.copy2(db_path, backup_path)

            messages.success(request, f'Backup creado exitosamente: {backup_filename}')
        except Exception as e:
            messages.error(request, f'Error al crear backup: {str(e)}')

        return redirect('administrador:backup_database')

    # Listar backups existentes
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []

    if os.path.exists(backup_dir):
        for filename in sorted(os.listdir(backup_dir), reverse=True):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                backups.append({
                    'nombre': filename,
                    'tamano': f'{size / 1024 / 1024:.2f} MB',
                    'fecha': datetime.fromtimestamp(mtime).strftime('%d/%m/%Y %H:%M:%S')
                })

    context = {
        'titulo': 'Backup de Base de Datos',
        'seccion': 'backup',
        'backups': backups
    }
    return render(request, 'administrador/backup_database.html', context)


@login_required
@admin_required
def backup_restore(request):
    """Vista para restaurar backup"""
    import os
    from django.conf import settings
    from datetime import datetime

    if request.method == 'POST':
        backup_file = request.POST.get('backup_file')

        if backup_file:
            try:
                backup_dir = os.path.join(settings.BASE_DIR, 'backups')
                backup_path = os.path.join(backup_dir, backup_file)

                if os.path.exists(backup_path):
                    messages.success(request, f'Backup {backup_file} listo para restaurar. Contacte al administrador del sistema.')
                else:
                    messages.error(request, 'Archivo de backup no encontrado.')
            except Exception as e:
                messages.error(request, f'Error al preparar restauración: {str(e)}')

        return redirect('administrador:backup_restore')

    # Listar backups disponibles
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backups = []

    if os.path.exists(backup_dir):
        for filename in sorted(os.listdir(backup_dir), reverse=True):
            if filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                backups.append({
                    'nombre': filename,
                    'tamano': f'{size / 1024 / 1024:.2f} MB',
                    'fecha': datetime.fromtimestamp(mtime).strftime('%d/%m/%Y %H:%M:%S')
                })

    context = {
        'titulo': 'Restaurar Backup',
        'seccion': 'backup',
        'backups': backups
    }
    return render(request, 'administrador/backup_restore.html', context)


@login_required
@admin_required
def backup_download(request, filename):
    """Vista para descargar un backup"""
    import os
    from django.conf import settings
    from django.http import FileResponse, Http404

    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backup_path = os.path.join(backup_dir, filename)

    if os.path.exists(backup_path) and filename.endswith('.db'):
        response = FileResponse(open(backup_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        raise Http404("Archivo de backup no encontrado")
