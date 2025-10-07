from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from datetime import timedelta

class PerfilUsuario(models.Model):
    """Modelo extendido para usuarios del sistema"""

    TIPO_USUARIO_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMINISTRADOR', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('TECNICO', 'Técnico'),
        ('PROVEEDOR', 'Proveedor'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, verbose_name="Tipo de Usuario")
    telefono = models.CharField(max_length=17, blank=True, null=True, verbose_name="Teléfono")
    documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="Documento")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")

    # Permisos especiales
    puede_crear_usuarios = models.BooleanField(default=False, verbose_name="Puede crear usuarios")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='usuarios_creados', verbose_name="Creado por")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        db_table = 'perfil_usuario'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_tipo_usuario_display()}"

    @property
    def esta_activo(self):
        return self.estado == 'ACTIVO' and self.user.is_active


class TokenRecuperacion(models.Model):
    """Tokens para recuperación de contraseña"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens_recuperacion')
    token = models.CharField(max_length=100, unique=True, verbose_name="Token")
    codigo = models.CharField(max_length=6, verbose_name="Código de Verificación")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_expiracion = models.DateTimeField(verbose_name="Fecha de Expiración")
    usado = models.BooleanField(default=False, verbose_name="Usado")
    ip_solicitud = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP de Solicitud")

    class Meta:
        verbose_name = "Token de Recuperación"
        verbose_name_plural = "Tokens de Recuperación"
        db_table = 'tokens_recuperacion'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Token para {self.user.username} - {self.codigo}"

    @classmethod
    def crear_token(cls, user):
        """Crea un nuevo token de recuperación"""
        token = secrets.token_urlsafe(32)
        codigo = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        fecha_expiracion = timezone.now() + timedelta(hours=1)

        return cls.objects.create(
            user=user,
            token=token,
            codigo=codigo,
            fecha_expiracion=fecha_expiracion
        )

    def es_valido(self):
        """Verifica si el token es válido"""
        return not self.usado and timezone.now() < self.fecha_expiracion

    def marcar_usado(self):
        """Marca el token como usado"""
        self.usado = True
        self.save()


class HistorialAcceso(models.Model):
    """Registro de accesos al sistema"""

    TIPO_ACCION_CHOICES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('LOGIN_FALLIDO', 'Intento Fallido'),
        ('RECUPERACION', 'Recuperación de Contraseña'),
        ('CAMBIO_PASSWORD', 'Cambio de Contraseña'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='historial_accesos')
    tipo_accion = models.CharField(max_length=20, choices=TIPO_ACCION_CHOICES, verbose_name="Tipo de Acción")
    username = models.CharField(max_length=150, verbose_name="Usuario")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="Navegador")
    exitoso = models.BooleanField(default=True, verbose_name="Exitoso")
    mensaje = models.TextField(blank=True, null=True, verbose_name="Mensaje")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Historial de Acceso"
        verbose_name_plural = "Historial de Accesos"
        db_table = 'historial_accesos'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.username} - {self.get_tipo_accion_display()} - {self.fecha}"

    @classmethod
    def registrar_acceso(cls, request, tipo_accion, user=None, exitoso=True, mensaje=''):
        """Registra un acceso al sistema"""
        username = user.username if user else request.POST.get('username', 'Desconocido')

        # Obtener IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        return cls.objects.create(
            user=user,
            tipo_accion=tipo_accion,
            username=username,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            exitoso=exitoso,
            mensaje=mensaje
        )

