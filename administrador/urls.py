"""
DigitSoft - Módulo de Administrador
URLs

Define las rutas del módulo de administración.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.urls import path
from . import views, ecommerce, reportes

app_name = 'administrador'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),

    # Configuración
    path('configuracion/', views.configuracion, name='configuracion'),

    # Logs de actividad
    path('logs/', views.logs_actividad, name='logs'),

    # ========================================================================
    # MÓDULOS DE GESTIÓN DE PRODUCTOS
    # ========================================================================
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),

    # ========================================================================
    # MÓDULOS DE COMPRAS
    # ========================================================================
    path('compras/', views.compra_list, name='compra_list'),
    path('compras/crear/', views.compra_create, name='compra_create'),
    path('compras/<int:pk>/detalle/', views.compra_detail, name='compra_detail'),

    # ========================================================================
    # MÓDULOS DE VENTAS
    # ========================================================================
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/crear/', views.venta_create, name='venta_create'),
    path('ventas/<int:pk>/detalle/', views.venta_detail, name='venta_detail'),

    # ========================================================================
    # MÓDULOS DE CLIENTES
    # ========================================================================
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),

    # ========================================================================
    # MÓDULOS DE EQUIPOS
    # ========================================================================
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('equipos/crear/', views.equipo_create, name='equipo_create'),
    path('equipos/<int:pk>/editar/', views.equipo_update, name='equipo_update'),
    path('equipos/<int:pk>/eliminar/', views.equipo_delete, name='equipo_delete'),

    # ========================================================================
    # MÓDULOS DE FACTURACIÓN
    # ========================================================================
    path('facturacion/', views.facturacion_list, name='facturacion_list'),
    path('facturacion/crear/', views.facturacion_create, name='facturacion_create'),
    path('facturacion/<int:pk>/detalle/', views.facturacion_detail, name='facturacion_detail'),
    path('facturacion/<int:pk>/pdf/', views.facturacion_pdf, name='facturacion_pdf'),

    # ========================================================================
    # MÓDULOS DE GARANTÍAS
    # ========================================================================
    path('garantias/', views.garantia_list, name='garantia_list'),
    path('garantias/crear/', views.garantia_create, name='garantia_create'),
    path('garantias/<int:pk>/detalle/', views.garantia_detail, name='garantia_detail'),
    path('garantias/mis-garantias/', views.mis_garantias, name='mis_garantias'),

    # ========================================================================
    # MÓDULOS DE MARCAS
    # ========================================================================
    path('marcas/', views.marca_list, name='marca_list'),
    path('marcas/crear/', views.marca_create, name='marca_create'),
    path('marcas/<int:pk>/editar/', views.marca_update, name='marca_update'),
    path('marcas/<int:pk>/eliminar/', views.marca_delete, name='marca_delete'),

    # ========================================================================
    # MÓDULOS DE PROVEEDORES
    # ========================================================================
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/crear/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),

    # ========================================================================
    # MÓDULOS DE TÉCNICOS
    # ========================================================================
    path('tecnicos/', views.tecnico_list, name='tecnico_list'),
    path('tecnicos/crear/', views.tecnico_create, name='tecnico_create'),
    path('tecnicos/<int:pk>/editar/', views.tecnico_update, name='tecnico_update'),
    path('tecnicos/<int:pk>/eliminar/', views.tecnico_delete, name='tecnico_delete'),

    # ========================================================================
    # MÓDULOS DE TIENDA ONLINE (Administración)
    # ========================================================================
    path('tienda/', views.tienda_list, name='tienda_list'),
    path('tienda/configuracion/', views.tienda_config, name='tienda_config'),

    # ========================================================================
    # MÓDULOS DE ÓRDENES DE SERVICIO
    # ========================================================================
    path('ordenes-servicio/', views.orden_servicio_list, name='orden_servicio_list'),
    path('ordenes-servicio/crear/', views.orden_servicio_create, name='orden_servicio_create'),
    path('ordenes-servicio/<int:pk>/detalle/', views.orden_servicio_detail, name='orden_servicio_detail'),
    path('ordenes-servicio/<int:pk>/editar/', views.orden_servicio_update, name='orden_servicio_update'),

    # ========================================================================
    # MÓDULOS DE SERVICIOS TÉCNICOS
    # ========================================================================
    path('servicios-tecnicos/', views.servicio_tecnico_list, name='servicio_tecnico_list'),
    path('servicios-tecnicos/crear/', views.servicio_tecnico_create, name='servicio_tecnico_create'),
    path('servicios-tecnicos/<int:pk>/detalle/', views.servicio_tecnico_detail, name='servicio_tecnico_detail'),

    # ========================================================================
    # MÓDULOS DE CARRITOS
    # ========================================================================
    path('carritos/', views.carrito_list, name='carrito_list'),
    path('carritos/<int:pk>/detalle/', views.carrito_detail, name='carrito_detail'),

    # ========================================================================
    # E-COMMERCE - VISTAS PÚBLICAS
    # ========================================================================
    path('tienda-publica/', ecommerce.tienda_publica, name='tienda_publica'),
    path('ver-carrito/', ecommerce.ver_carrito, name='ver_carrito'),
    path('mis-compras/', ecommerce.mis_compras, name='mis_compras'),

    # ========================================================================
    # MÓDULOS DE REPORTES
    # ========================================================================
    path('reportes/', reportes.reportes_dashboard, name='reportes_dashboard'),
    path('reportes/ventas/', reportes.reporte_ventas, name='reporte_ventas'),
    path('reportes/inventario/', reportes.reporte_inventario, name='reporte_inventario'),
    path('reportes/servicios/', reportes.reporte_servicios, name='reporte_servicios'),

    # ========================================================================
    # MÓDULOS DE AYUDA
    # ========================================================================
    path('ayuda/', views.ayuda_faq, name='ayuda_faq'),
    path('ayuda/manual/', views.ayuda_manual, name='ayuda_manual'),

    # ========================================================================
    # MÓDULOS DE BACKUP
    # ========================================================================
    path('backup/', views.backup_database, name='backup_database'),
    path('backup/restaurar/', views.backup_restore, name='backup_restore'),
]
