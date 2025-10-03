from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('facturacion/', views.facturacion_list, name='facturacion_list'),
    path('garantias/', views.garantia_list, name='garantia_list'),
    path('marcas/', views.marca_list, name='marca_list'),
    path('ordenes-servicio/', views.orden_servicio_list, name='orden_servicio_list'),
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('servicios-tecnicos/', views.servicio_tecnico_list, name='servicio_tecnico_list'),
    path('tecnicos/', views.tecnico_list, name='tecnico_list'),
    path('ventas/', views.venta_list, name='venta_list'),
    path('productos/', views.producto_list, name='producto_list'),
]
