# ========================================================================
# GESTIÓN DE CLIENTES - VERSIÓN CORREGIDA
# ========================================================================
@login_required
@admin_required
def cliente_list(request):
    """Vista para listar clientes"""
    from clientes.models import Cliente
    clientes = Cliente.objects.all().select_related('user').order_by('-fecha_registro')

    context = {
        'titulo': 'Gestión de Clientes',
        'seccion': 'clientes',
        'clientes': clientes
    }
    return render(request, 'administrador/cliente_list.html', context)


@login_required
@admin_required
def cliente_create(request):
    """Vista para crear cliente"""
    from clientes.models import Cliente
    from django.contrib.auth.models import User

    if request.method == 'POST':
        try:
            # Crear usuario si se proporciona email y contraseña
            email = request.POST.get('email')
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos', '')
            tipo_documento = request.POST.get('tipo_documento')
            numero_documento = request.POST.get('numero_documento')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion', '')
            ciudad = request.POST.get('ciudad', '')
            departamento = request.POST.get('departamento', '')

            # Verificar si el documento ya existe
            if Cliente.objects.filter(numero_documento=numero_documento).exists():
                messages.error(request, f'Ya existe un cliente con el documento {numero_documento}')
                return redirect('administrador:cliente_create')

            # Crear el cliente
            cliente = Cliente.objects.create(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombres=nombres,
                apellidos=apellidos,
                email=email,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                departamento=departamento,
                tipo_cliente=request.POST.get('tipo_cliente', 'NATURAL'),
                activo=True
            )

            messages.success(request, f'Cliente "{nombres} {apellidos}" creado exitosamente.')
            return redirect('administrador:cliente_list')

        except Exception as e:
            messages.error(request, f'Error al crear cliente: {str(e)}')
            return redirect('administrador:cliente_create')

    context = {
        'titulo': 'Nuevo Cliente',
        'seccion': 'clientes'
    }
    return render(request, 'administrador/cliente_form.html', context)


@login_required
@admin_required
def cliente_update(request, pk):
    """Vista para actualizar cliente"""
    from clientes.models import Cliente
    from django.shortcuts import get_object_or_404

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            cliente.nombres = request.POST.get('nombres')
            cliente.apellidos = request.POST.get('apellidos', '')
            cliente.email = request.POST.get('email')
            cliente.telefono = request.POST.get('telefono')
            cliente.direccion = request.POST.get('direccion', '')
            cliente.ciudad = request.POST.get('ciudad', '')
            cliente.departamento = request.POST.get('departamento', '')
            cliente.tipo_cliente = request.POST.get('tipo_cliente', 'NATURAL')
            cliente.activo = request.POST.get('activo') == 'on'
            cliente.save()

            messages.success(request, f'Cliente "{cliente.nombres}" actualizado exitosamente.')
            return redirect('administrador:cliente_list')

        except Exception as e:
            messages.error(request, f'Error al actualizar cliente: {str(e)}')

    context = {
        'titulo': 'Editar Cliente',
        'seccion': 'clientes',
        'cliente': cliente
    }
    return render(request, 'administrador/cliente_form.html', context)


@login_required
@admin_required
def cliente_delete(request, pk):
    """Vista para eliminar cliente"""
    from clientes.models import Cliente
    from django.shortcuts import get_object_or_404

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            nombre_completo = f"{cliente.nombres} {cliente.apellidos}"
            cliente.delete()
            messages.success(request, f'Cliente "{nombre_completo}" eliminado exitosamente.')
            return redirect('administrador:cliente_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar cliente: {str(e)}')
            return redirect('administrador:cliente_list')

    context = {
        'titulo': 'Eliminar Cliente',
        'seccion': 'clientes',
        'cliente': cliente
    }
    return render(request, 'administrador/cliente_confirm_delete.html', context)

