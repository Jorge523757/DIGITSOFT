from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Gestión de Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/<int:cliente_id>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:cliente_id>/delete/', views.cliente_delete, name='cliente_delete'),

    # Gestión de Productos
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/<int:producto_id>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:producto_id>/edit/', views.producto_edit, name='producto_edit'),
    path('productos/<int:producto_id>/delete/', views.producto_delete, name='producto_delete'),

    # Gestión de Equipos
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('equipos/<int:equipo_id>/', views.equipo_detail, name='equipo_detail'),
    path('equipos/<int:equipo_id>/delete/', views.equipo_delete, name='equipo_delete'),

    # Gestión de Marcas
    path('marcas/', views.marca_list, name='marca_list'),
    path('marcas/<int:marca_id>/', views.marca_detail, name='marca_detail'),
    path('marcas/<int:marca_id>/delete/', views.marca_delete, name='marca_delete'),

    # Gestión de Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/<int:proveedor_id>/', views.proveedor_detail, name='proveedor_detail'),
    path('proveedores/<int:proveedor_id>/delete/', views.proveedor_delete, name='proveedor_delete'),

    # Gestión de Técnicos
    path('tecnicos/', views.tecnico_list, name='tecnico_list'),
    path('tecnicos/<int:tecnico_id>/', views.tecnico_detail, name='tecnico_detail'),
    path('tecnicos/<int:tecnico_id>/delete/', views.tecnico_delete, name='tecnico_delete'),

    # Órdenes de Servicio
    path('orden-servicio/', views.orden_servicio_list, name='orden_servicio_list'),
    path('orden-servicio/<int:orden_id>/', views.orden_servicio_detail, name='orden_servicio_detail'),

    # Servicios Técnicos
    path('servicios-tecnicos/', views.servicio_tecnico_list, name='servicio_tecnico_list'),

    # Gestión de Compras
    path('compras/', views.compra_list, name='compra_list'),
    path('compras/<int:compra_id>/', views.compra_detail, name='compra_detail'),
    path('compras/pendientes/', views.compras_pendientes, name='compras_pendientes'),

    # Gestión de Carritos
    path('carritos/', views.carrito_list, name='carrito_list'),
    path('carritos/<int:carrito_id>/', views.carrito_detail, name='carrito_detail'),
    path('carritos/abandonados/', views.carritos_abandonados, name='carritos_abandonados'),

    # Gestión de Ventas
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/<int:venta_id>/', views.venta_detail, name='venta_detail'),

    # Facturación
    path('facturacion/', views.facturacion_list, name='facturacion_list'),

    # Garantías
    path('garantias/', views.garantia_list, name='garantia_list'),
    path('garantias/<int:garantia_id>/', views.garantia_detail, name='garantia_detail'),

    # Administradores
    path('administradores/', views.administrador_list, name='administrador_list'),

    # Tienda Online
    path('tienda/', views.tienda_list, name='tienda_list'),
    path('tienda/<int:producto_id>/toggle/', views.tienda_producto_toggle, name='tienda_producto_toggle'),
]
