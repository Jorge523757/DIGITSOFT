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

    # Gestión de Equipos
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('equipos/<int:equipo_id>/', views.equipo_detail, name='equipo_detail'),

    # Gestión de Productos
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/<int:producto_id>/', views.producto_detail, name='producto_detail'),

    # Gestión de Marcas
    path('marcas/', views.marca_list, name='marca_list'),
    path('marcas/<int:marca_id>/', views.marca_detail, name='marca_detail'),

    # Gestión de Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/<int:proveedor_id>/', views.proveedor_detail, name='proveedor_detail'),

    # Gestión de Técnicos
    path('tecnicos/', views.tecnico_list, name='tecnico_list'),
    path('tecnicos/<int:tecnico_id>/', views.tecnico_detail, name='tecnico_detail'),

    # Órdenes de Servicio
    path('orden-servicio/', views.orden_servicio_list, name='orden_servicio_list'),
    path('orden-servicio/<int:orden_id>/', views.orden_servicio_detail, name='orden_servicio_detail'),

    # Servicios Técnicos
    path('servicios-tecnicos/', views.servicio_tecnico_list, name='servicio_tecnico_list'),
    path('servicios-tecnicos/<int:servicio_id>/', views.servicio_tecnico_detail, name='servicio_tecnico_detail'),

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
    path('facturacion/<int:factura_id>/', views.factura_detail, name='factura_detail'),

    # Garantías
    path('garantias/', views.garantia_list, name='garantia_list'),
    path('garantias/<int:garantia_id>/', views.garantia_detail, name='garantia_detail'),

    # Logs y Auditoría
    path('logs/', views.log_actividad_list, name='log_actividad_list'),

    # Configuración
    path('configuracion/', views.configuracion_general, name='configuracion_general'),
]
