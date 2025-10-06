from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pagina-principal/', views.pagina_principal, name='pagina_principal'),

    # Tienda Online y Ecommerce
    path('tienda/', views.tienda, name='tienda'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),

    # Carrito de Compras
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),

    # Otras páginas
    path('portafolio/', views.portafolio, name='portafolio'),
    path('servicios/', views.servicios, name='servicios'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
]
