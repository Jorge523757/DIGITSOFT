"""
Módulo de Reportes - Digit Soft
Sistema de generación de reportes en PDF y Excel
"""
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import csv
from .models import (
    Cliente, Producto, Venta, Compra, OrdenServicio,
    Equipo, Tecnico, Proveedor, Factura
)


# ========== REPORTES EN CSV/EXCEL ========== #

def generar_reporte_ventas_csv(request):
    """Genera reporte de ventas en formato CSV"""
    # Obtener parámetros de filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Crear respuesta HTTP con CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reporte_ventas_{timezone.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf-8'))  # BOM para Excel

    writer = csv.writer(response)

    # Encabezados
    writer.writerow([
        'Número Venta',
        'Fecha',
        'Cliente',
        'Vendedor',
        'Subtotal',
        'Descuento',
        'Impuestos',
        'Total',
        'Método Pago',
        'Estado'
    ])

    # Filtrar ventas
    ventas = Venta.objects.select_related('cliente', 'vendedor').all()

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=fecha_fin)

    # Escribir datos
    total_ventas = 0
    for venta in ventas:
        writer.writerow([
            venta.numero_venta,
            venta.fecha_venta.strftime('%d/%m/%Y %H:%M'),
            venta.cliente.nombre_completo if venta.cliente else 'N/A',
            venta.vendedor.nombre_completo if venta.vendedor else 'N/A',
            f'${venta.subtotal:,.2f}',
            f'${venta.descuento:,.2f}',
            f'${venta.impuestos:,.2f}',
            f'${venta.total:,.2f}',
            venta.get_metodo_pago_display(),
            venta.get_estado_display()
        ])
        total_ventas += venta.total

    # Total general
    writer.writerow([])
    writer.writerow(['TOTAL GENERAL', '', '', '', '', '', '', f'${total_ventas:,.2f}', '', ''])

    return response


def generar_reporte_inventario_csv(request):
    """Genera reporte de inventario en formato CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reporte_inventario_{timezone.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)

    # Encabezados
    writer.writerow([
        'Código',
        'Nombre',
        'Categoría',
        'Marca',
        'Stock Actual',
        'Stock Mínimo',
        'Stock Máximo',
        'Precio Compra',
        'Precio Venta',
        'Valor Inventario',
        'Estado'
    ])

    # Productos
    productos = Producto.objects.select_related('marca').filter(activo=True)

    total_valor = 0
    productos_bajo_stock = 0

    for producto in productos:
        valor_inventario = producto.precio_venta * producto.stock_actual
        total_valor += valor_inventario

        if producto.stock_actual <= producto.stock_minimo:
            productos_bajo_stock += 1

        writer.writerow([
            producto.codigo_producto,
            producto.nombre,
            producto.get_categoria_display(),
            producto.marca.nombre if producto.marca else 'N/A',
            producto.stock_actual,
            producto.stock_minimo,
            producto.stock_maximo,
            f'${producto.precio_compra:,.2f}',
            f'${producto.precio_venta:,.2f}',
            f'${valor_inventario:,.2f}',
            producto.get_estado_display()
        ])

    # Resumen
    writer.writerow([])
    writer.writerow(['RESUMEN DEL INVENTARIO'])
    writer.writerow(['Total de Productos:', productos.count()])
    writer.writerow(['Productos con Stock Bajo:', productos_bajo_stock])
    writer.writerow(['Valor Total del Inventario:', f'${total_valor:,.2f}'])

    return response


def generar_reporte_clientes_csv(request):
    """Genera reporte de clientes en formato CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reporte_clientes_{timezone.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)

    # Encabezados
    writer.writerow([
        'Tipo Documento',
        'Número Documento',
        'Nombre Completo',
        'Tipo Cliente',
        'Teléfono',
        'Email',
        'Ciudad',
        'Departamento',
        'Fecha Registro',
        'Estado'
    ])

    # Clientes
    clientes = Cliente.objects.filter(activo=True).order_by('nombres')

    for cliente in clientes:
        writer.writerow([
            cliente.get_tipo_documento_display(),
            cliente.numero_documento,
            cliente.nombre_completo,
            cliente.get_tipo_cliente_display(),
            cliente.telefono,
            cliente.email,
            cliente.ciudad,
            cliente.departamento,
            cliente.fecha_registro.strftime('%d/%m/%Y'),
            'Activo' if cliente.activo else 'Inactivo'
        ])

    # Resumen
    writer.writerow([])
    writer.writerow(['TOTAL DE CLIENTES:', clientes.count()])
    writer.writerow([
        'Personas Naturales:',
        clientes.filter(tipo_cliente='NATURAL').count()
    ])
    writer.writerow([
        'Personas Jurídicas:',
        clientes.filter(tipo_cliente='JURIDICA').count()
    ])

    return response


def generar_reporte_servicios_csv(request):
    """Genera reporte de órdenes de servicio en formato CSV"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reporte_servicios_{timezone.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)

    # Encabezados
    writer.writerow([
        'Número Orden',
        'Cliente',
        'Equipo',
        'Técnico',
        'Fecha Ingreso',
        'Fecha Entrega',
        'Estado',
        'Prioridad',
        'Costo Mano Obra',
        'Costo Repuestos',
        'Total'
    ])

    # Filtrar órdenes
    ordenes = OrdenServicio.objects.select_related('cliente', 'equipo', 'tecnico_asignado').all()

    if fecha_inicio:
        ordenes = ordenes.filter(fecha_ingreso__gte=fecha_inicio)
    if fecha_fin:
        ordenes = ordenes.filter(fecha_ingreso__lte=fecha_fin)

    total_mano_obra = 0
    total_repuestos = 0
    total_general = 0

    for orden in ordenes:
        writer.writerow([
            orden.numero_orden,
            orden.cliente.nombre_completo if orden.cliente else 'N/A',
            orden.equipo.nombre if orden.equipo else 'N/A',
            orden.tecnico_asignado.nombre_completo if orden.tecnico_asignado else 'Sin asignar',
            orden.fecha_ingreso.strftime('%d/%m/%Y'),
            orden.fecha_entrega_real.strftime('%d/%m/%Y') if orden.fecha_entrega_real else 'Pendiente',
            orden.get_estado_display(),
            orden.get_prioridad_display(),
            f'${orden.costo_mano_obra:,.2f}',
            f'${orden.costo_repuestos:,.2f}',
            f'${orden.total:,.2f}'
        ])
        total_mano_obra += orden.costo_mano_obra
        total_repuestos += orden.costo_repuestos
        total_general += orden.total

    # Totales
    writer.writerow([])
    writer.writerow(['TOTALES', '', '', '', '', '', '', '',
                    f'${total_mano_obra:,.2f}',
                    f'${total_repuestos:,.2f}',
                    f'${total_general:,.2f}'])

    return response


def generar_reporte_compras_csv(request):
    """Genera reporte de compras en formato CSV"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reporte_compras_{timezone.now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)

    # Encabezados
    writer.writerow([
        'Número Compra',
        'Proveedor',
        'Fecha Solicitud',
        'Estado',
        'Subtotal',
        'Descuento',
        'Impuestos',
        'Costos Envío',
        'Total',
        'Método Pago'
    ])

    # Filtrar compras
    compras = Compra.objects.select_related('proveedor').all()

    if fecha_inicio:
        compras = compras.filter(fecha_solicitud__gte=fecha_inicio)
    if fecha_fin:
        compras = compras.filter(fecha_solicitud__lte=fecha_fin)

    total_compras = 0

    for compra in compras:
        writer.writerow([
            compra.numero_compra,
            compra.proveedor.razon_social if compra.proveedor else 'N/A',
            compra.fecha_solicitud.strftime('%d/%m/%Y'),
            compra.get_estado_display(),
            f'${compra.subtotal:,.2f}',
            f'${compra.descuento:,.2f}',
            f'${compra.impuestos:,.2f}',
            f'${compra.costos_envio:,.2f}',
            f'${compra.total:,.2f}',
            compra.get_metodo_pago_display() if compra.metodo_pago else 'N/A'
        ])
        total_compras += compra.total

    # Total
    writer.writerow([])
    writer.writerow(['TOTAL COMPRAS', '', '', '', '', '', '', '', f'${total_compras:,.2f}', ''])

    return response


# ========== FUNCIONES DE ANÁLISIS ========== #

def obtener_estadisticas_ventas(fecha_inicio=None, fecha_fin=None):
    """Obtiene estadísticas de ventas para reportes"""
    ventas = Venta.objects.all()

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=fecha_fin)

    stats = ventas.aggregate(
        total_ventas=Count('id'),
        total_ingresos=Sum('total'),
        promedio_venta=Avg('total'),
        total_descuentos=Sum('descuento'),
        total_impuestos=Sum('impuestos')
    )

    return stats


def obtener_productos_mas_vendidos(limite=10):
    """Obtiene los productos más vendidos"""
    # Nota: Requiere modelo DetalleVenta que no está en el código actual
    # Por ahora retorna productos con stock bajo como indicador
    return Producto.objects.filter(activo=True).order_by('stock_actual')[:limite]


def obtener_clientes_frecuentes(limite=10):
    """Obtiene los clientes más frecuentes"""
    return Cliente.objects.annotate(
        total_compras=Count('venta')
    ).order_by('-total_compras')[:limite]

