from django.shortcuts import render

# Create your views here.

def cliente_list(request):
    return render(request, 'administrador/cliente_list.html')

def equipo_list(request):
    return render(request, 'administrador/equipo_list.html')

def facturacion_list(request):
    return render(request, 'administrador/facturacion_list.html')

def garantia_list(request):
    return render(request, 'administrador/garantia_list.html')

def marca_list(request):
    return render(request, 'administrador/marca_list.html')

def orden_servicio_list(request):
    return render(request, 'administrador/orden_servicio_list.html')

def proveedor_list(request):
    return render(request, 'administrador/proveedor_list.html')

def servicio_tecnico_list(request):
    return render(request, 'administrador/servicio_tecnico_list.html')

def tecnico_list(request):
    return render(request, 'administrador/tecnico_list.html')

def venta_list(request):
    return render(request, 'administrador/venta_list.html')

def producto_list(request):
    return render(request, 'administrador/producto_list.html')

def dashboard(request):
    return render(request, 'administrador/dashboard.html')
