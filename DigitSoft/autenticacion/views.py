from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import PerfilUsuario, TokenRecuperacion, HistorialAcceso
from .forms import LoginForm, RegistroUsuarioForm, RecuperacionPasswordForm, VerificarCodigoForm, NuevaPasswordForm, RegistroPublicoForm

def login_view(request):
    """Vista de inicio de sesión"""

    # Si el usuario ya está autenticado, redirigir según tipo
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
            if perfil.tipo_usuario in ['SUPER_ADMIN', 'ADMINISTRADOR']:
                return redirect('administrador:dashboard')
            else:
                return redirect('main:pagina_principal')
        except:
            return redirect('main:pagina_principal')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            # Intentar autenticar
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Verificar si tiene perfil y está activo
                try:
                    perfil = user.perfil
                    if perfil.esta_activo:
                        login(request, user)

                        # Configurar sesión
                        if not remember_me:
                            request.session.set_expiry(0)

                        # Registrar acceso exitoso
                        HistorialAcceso.registrar_acceso(
                            request,
                            'LOGIN',
                            user=user,
                            exitoso=True,
                            mensaje='Inicio de sesión exitoso'
                        )

                        # Mensaje de bienvenida con tipo de usuario
                        tipo_usuario_display = perfil.get_tipo_usuario_display()
                        messages.success(
                            request,
                            f'¡Bienvenido {user.get_full_name() or user.username}! '
                            f'Has iniciado sesión como {tipo_usuario_display}.'
                        )

                        # Redirigir según tipo de usuario
                        if perfil.tipo_usuario in ['SUPER_ADMIN', 'ADMINISTRADOR']:
                            return redirect('administrador:dashboard')
                        else:
                            # Clientes, Técnicos y Proveedores van a la página principal
                            return redirect('main:pagina_principal')
                    else:
                        messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
                        HistorialAcceso.registrar_acceso(
                            request,
                            'LOGIN_FALLIDO',
                            user=user,
                            exitoso=False,
                            mensaje='Cuenta inactiva'
                        )
                except PerfilUsuario.DoesNotExist:
                    messages.error(request, 'Tu cuenta no tiene un perfil asignado. Contacta al administrador.')
                    HistorialAcceso.registrar_acceso(
                        request,
                        'LOGIN_FALLIDO',
                        user=user,
                        exitoso=False,
                        mensaje='Sin perfil asignado'
                    )
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
                HistorialAcceso.registrar_acceso(
                    request,
                    'LOGIN_FALLIDO',
                    exitoso=False,
                    mensaje='Credenciales incorrectas'
                )
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = LoginForm()

    return render(request, 'autenticacion/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vista de cierre de sesión"""

    # Registrar cierre de sesión
    HistorialAcceso.registrar_acceso(
        request,
        'LOGOUT',
        user=request.user,
        exitoso=True,
        mensaje='Cierre de sesión'
    )

    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('autenticacion:login')


@login_required
def registro_usuario_view(request):
    """Vista para registrar nuevos usuarios (solo administradores)"""

    # Verificar permisos
    try:
        if not request.user.perfil.puede_crear_usuarios:
            messages.error(request, 'No tienes permisos para crear usuarios.')
            return redirect('administrador:dashboard')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No tienes un perfil válido.')
        return redirect('administrador:dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear usuario
                    user = form.save(commit=False)
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()

                    # Crear perfil
                    perfil = PerfilUsuario.objects.create(
                        user=user,
                        tipo_usuario=form.cleaned_data['tipo_usuario'],
                        telefono=form.cleaned_data.get('telefono', ''),
                        documento=form.cleaned_data['documento'],
                        creado_por=request.user
                    )

                    # Asignar permisos según tipo de usuario
                    if form.cleaned_data['tipo_usuario'] == 'SUPER_ADMIN':
                        perfil.puede_crear_usuarios = True
                        perfil.save()
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                    elif form.cleaned_data['tipo_usuario'] == 'ADMINISTRADOR':
                        perfil.puede_crear_usuarios = True
                        perfil.save()
                        user.is_staff = True
                        user.save()

                    messages.success(request, f'Usuario {user.username} creado exitosamente.')

                    # Enviar correo de bienvenida (opcional)
                    try:
                        send_mail(
                            'Bienvenido a DigitSoft',
                            f'Hola {user.get_full_name()},\n\nTu cuenta ha sido creada exitosamente.\n\nUsuario: {user.username}\n\nSaludos,\nEquipo DigitSoft',
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=True,
                        )
                    except:
                        pass

                    return redirect('autenticacion:lista_usuarios')

            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'autenticacion/registro.html', {'form': form})


def recuperar_password_view(request):
    """Vista para solicitar recuperación de contraseña"""

    if request.method == 'POST':
        form = RecuperacionPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email, is_active=True)

                # Crear token de recuperación
                token = TokenRecuperacion.crear_token(user)

                # Enviar correo con el código
                try:
                    send_mail(
                        'Recuperación de Contraseña - DigitSoft',
                        f'Hola {user.get_full_name()},\n\nTu código de recuperación es: {token.codigo}\n\nEste código expira en 1 hora.\n\nSi no solicitaste este código, ignora este mensaje.\n\nSaludos,\nEquipo DigitSoft',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    # Registrar solicitud
                    HistorialAcceso.registrar_acceso(
                        request,
                        'RECUPERACION',
                        user=user,
                        exitoso=True,
                        mensaje='Código de recuperación enviado'
                    )

                    # Guardar token en sesión
                    request.session['recovery_token'] = token.token
                    request.session['recovery_email'] = email

                    messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
                    return redirect('autenticacion:verificar_codigo')

                except Exception as e:
                    messages.error(request, f'Error al enviar el correo: {str(e)}')

            except User.DoesNotExist:
                # Por seguridad, no revelar si el email existe o no
                messages.success(request, 'Si el correo existe, recibirás un código de verificación.')
    else:
        form = RecuperacionPasswordForm()

    return render(request, 'autenticacion/recuperar_password.html', {'form': form})


def verificar_codigo_view(request):
    """Vista para verificar el código de recuperación"""

    if 'recovery_token' not in request.session:
        messages.error(request, 'Sesión inválida. Por favor solicita un nuevo código.')
        return redirect('autenticacion:recuperar_password')

    if request.method == 'POST':
        form = VerificarCodigoForm(request.POST)

        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            token_str = request.session.get('recovery_token')

            try:
                token = TokenRecuperacion.objects.get(token=token_str, codigo=codigo)

                if token.es_valido():
                    # Código válido, permitir cambiar contraseña
                    request.session['verified_token'] = token.token
                    messages.success(request, 'Código verificado correctamente.')
                    return redirect('autenticacion:nueva_password')
                else:
                    messages.error(request, 'El código ha expirado o ya fue usado.')

            except TokenRecuperacion.DoesNotExist:
                messages.error(request, 'Código incorrecto.')
    else:
        form = VerificarCodigoForm()

    email = request.session.get('recovery_email', '')
    email_oculto = f"{email[:3]}***{email[email.find('@'):]}" if email else ''

    return render(request, 'autenticacion/verificar_codigo.html', {
        'form': form,
        'email_oculto': email_oculto
    })


def nueva_password_view(request):
    """Vista para establecer nueva contraseña"""

    if 'verified_token' not in request.session:
        messages.error(request, 'Sesión inválida. Por favor verifica tu código primero.')
        return redirect('autenticacion:recuperar_password')

    if request.method == 'POST':
        form = NuevaPasswordForm(request.POST)

        if form.is_valid():
            token_str = request.session.get('verified_token')

            try:
                token = TokenRecuperacion.objects.get(token=token_str)

                if token.es_valido():
                    # Cambiar contraseña
                    user = token.user
                    user.set_password(form.cleaned_data['password1'])
                    user.save()

                    # Marcar token como usado
                    token.marcar_usado()

                    # Registrar cambio
                    HistorialAcceso.registrar_acceso(
                        request,
                        'CAMBIO_PASSWORD',
                        user=user,
                        exitoso=True,
                        mensaje='Contraseña cambiada por recuperación'
                    )

                    # Limpiar sesión
                    if 'recovery_token' in request.session:
                        del request.session['recovery_token']
                    if 'recovery_email' in request.session:
                        del request.session['recovery_email']
                    if 'verified_token' in request.session:
                        del request.session['verified_token']

                    messages.success(request, 'Contraseña cambiada exitosamente. Ya puedes iniciar sesión.')
                    return redirect('autenticacion:login')
                else:
                    messages.error(request, 'El token ha expirado.')
                    return redirect('autenticacion:recuperar_password')

            except TokenRecuperacion.DoesNotExist:
                messages.error(request, 'Token inválido.')
                return redirect('autenticacion:recuperar_password')
    else:
        form = NuevaPasswordForm()

    return render(request, 'autenticacion/nueva_password.html', {'form': form})


@login_required
def lista_usuarios_view(request):
    """Vista para listar usuarios (solo administradores)"""

    # Verificar permisos
    try:
        if not request.user.perfil.puede_crear_usuarios:
            messages.error(request, 'No tienes permisos para ver esta página.')
            return redirect('administrador:dashboard')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No tienes un perfil válido.')
        return redirect('administrador:dashboard')

    usuarios = User.objects.select_related('perfil').all().order_by('-date_joined')

    return render(request, 'autenticacion/lista_usuarios.html', {'usuarios': usuarios})


@login_required
def toggle_estado_usuario(request, user_id):
    """Vista para activar/desactivar usuarios"""

    # Verificar permisos
    try:
        if not request.user.perfil.puede_crear_usuarios:
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('administrador:dashboard')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No tienes un perfil válido.')
        return redirect('administrador:dashboard')

    user = get_object_or_404(User, id=user_id)

    # No permitir que se desactive a sí mismo
    if user == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('autenticacion:lista_usuarios')

    try:
        perfil = user.perfil
        if perfil.estado == 'ACTIVO':
            perfil.estado = 'INACTIVO'
            user.is_active = False
            messages.success(request, f'Usuario {user.username} desactivado.')
        else:
            perfil.estado = 'ACTIVO'
            user.is_active = True
            messages.success(request, f'Usuario {user.username} activado.')

        perfil.save()
        user.save()

    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'El usuario no tiene perfil.')

    return redirect('autenticacion:lista_usuarios')


def registro_publico_view(request):
    """Vista para registro público de clientes"""

    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('administrador:dashboard')

    if request.method == 'POST':
        form = RegistroPublicoForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear usuario
                    user = form.save(commit=False)
                    user.email = form.cleaned_data['email']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()

                    # Crear perfil como CLIENTE
                    perfil = PerfilUsuario.objects.create(
                        user=user,
                        tipo_usuario='CLIENTE',
                        telefono=form.cleaned_data.get('telefono', ''),
                        documento=form.cleaned_data['documento'],
                        estado='ACTIVO'
                    )

                    # Registrar creación
                    HistorialAcceso.registrar_acceso(
                        request,
                        'REGISTRO',
                        user=user,
                        exitoso=True,
                        mensaje='Registro exitoso de nuevo cliente'
                    )

                    # Enviar correo de bienvenida
                    try:
                        send_mail(
                            'Bienvenido a DigitSoft',
                            f'Hola {user.get_full_name()},\n\n'
                            f'¡Gracias por registrarte en DigitSoft!\n\n'
                            f'Tu cuenta ha sido creada exitosamente.\n\n'
                            f'Usuario: {user.username}\n'
                            f'Tipo de cuenta: Cliente\n\n'
                            f'Ya puedes iniciar sesión en nuestro sistema.\n\n'
                            f'Saludos,\nEquipo DigitSoft',
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=True,
                        )
                    except:
                        pass

                    messages.success(
                        request,
                        f'¡Registro exitoso! Tu cuenta ha sido creada. Ya puedes iniciar sesión.'
                    )
                    return redirect('autenticacion:login')

            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroPublicoForm()

    return render(request, 'autenticacion/registro_publico.html', {'form': form})


@login_required
def perfil_usuario_view(request):
    """Vista para ver y editar el perfil del usuario"""

    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No tienes un perfil asignado.')
        return redirect('main:pagina_principal')

    if request.method == 'POST':
        # Actualizar datos del usuario
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        # Actualizar datos del perfil
        perfil.telefono = request.POST.get('telefono', '')
        perfil.direccion = request.POST.get('direccion', '')
        perfil.save()

        messages.success(request, 'Perfil actualizado exitosamente.')
        return redirect('autenticacion:perfil_usuario')

    context = {
        'perfil': perfil,
    }
    return render(request, 'autenticacion/perfil_usuario.html', context)


@login_required
def cambiar_password_view(request):
    """Vista para cambiar la contraseña del usuario"""

    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')

        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('autenticacion:perfil_usuario')

        # Verificar que las nuevas contraseñas coincidan
        if password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
            return redirect('autenticacion:perfil_usuario')

        # Verificar longitud mínima
        if len(password_nueva) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('autenticacion:perfil_usuario')

        # Cambiar contraseña
        request.user.set_password(password_nueva)
        request.user.save()

        # Registrar cambio
        HistorialAcceso.registrar_acceso(
            request,
            'CAMBIO_PASSWORD',
            user=request.user,
            exitoso=True,
            mensaje='Contraseña cambiada desde perfil'
        )

        # Mantener la sesión activa
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Contraseña cambiada exitosamente.')
        return redirect('autenticacion:perfil_usuario')

    return redirect('autenticacion:perfil_usuario')
