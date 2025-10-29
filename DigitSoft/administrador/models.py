"""
DigitSoft - Módulo de Administrador
Models

Define los modelos de datos para la gestión de administradores.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.db import models
from django.contrib.auth.models import User

# ========== MODELO DE ADMINISTRADOR ========== #
class Administrador(models.Model):
    """Modelo extendido para usuarios administradores"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cargo}"


# ========== LOG DE ACTIVIDADES ========== #
class LogActividad(models.Model):
    """Modelo para registrar actividades de los administradores"""
    TIPO_ACTIVIDAD_CHOICES = [
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('CREAR', 'Crear Registro'),
        ('EDITAR', 'Editar Registro'),
        ('ELIMINAR', 'Eliminar Registro'),
        ('VER', 'Ver Registro'),
        ('EXPORTAR', 'Exportar Datos'),
        ('APROBAR', 'Aprobar Proceso'),
        ('RECHAZAR', 'Rechazar Proceso'),
        ('CONFIGURAR', 'Configurar Sistema'),
    ]

    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, verbose_name="Administrador")
    tipo_actividad = models.CharField(max_length=15, choices=TIPO_ACTIVIDAD_CHOICES, verbose_name="Tipo de actividad")
    descripcion = models.TextField(verbose_name="Descripción de la actividad")

    modulo_afectado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Módulo afectado")
    registro_afectado_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="ID del registro afectado")

    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Dirección IP")
    user_agent = models.TextField(blank=True, null=True, verbose_name="Navegador/User Agent")

    fecha_actividad = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la actividad")

    class Meta:
        verbose_name = "Log de Actividad"
        verbose_name_plural = "Logs de Actividad"
        ordering = ['-fecha_actividad']
        db_table = 'logs_actividad'

    def __str__(self):
        return f"{self.administrador} - {self.get_tipo_actividad_display()} - {self.fecha_actividad}"


# ========== CONFIGURACIÓN GENERAL ========== #
class ConfiguracionGeneral(models.Model):
    """Configuraciones generales del sistema"""
    empresa_nombre = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    empresa_nit = models.CharField(max_length=20, verbose_name="NIT de la empresa")
    empresa_direccion = models.TextField(verbose_name="Dirección de la empresa")
    empresa_telefono = models.CharField(max_length=17, verbose_name="Teléfono de la empresa")
    empresa_email = models.EmailField(verbose_name="Email de la empresa")
    empresa_logo = models.ImageField(upload_to='empresa/', blank=True, null=True, verbose_name="Logo de la empresa")

    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, verbose_name="IVA (%)")
    moneda = models.CharField(max_length=10, default='COP', verbose_name="Moneda")
    timezone = models.CharField(max_length=50, default='America/Bogota', verbose_name="Zona horaria")

    # Configuraciones de facturación
    resolucion_dian = models.CharField(max_length=100, blank=True, null=True, verbose_name="Resolución DIAN")
    rango_numeracion_desde = models.PositiveIntegerField(default=1, verbose_name="Numeración desde")
    rango_numeracion_hasta = models.PositiveIntegerField(default=100000, verbose_name="Numeración hasta")
    prefijo_factura = models.CharField(max_length=10, default='FAC', verbose_name="Prefijo factura")

    # Configuraciones de notificaciones
    email_smtp_server = models.CharField(max_length=100, blank=True, null=True, verbose_name="Servidor SMTP")
    email_smtp_port = models.PositiveIntegerField(default=587, verbose_name="Puerto SMTP")
    email_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Usuario email")
    email_password = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contraseña email")
    email_use_tls = models.BooleanField(default=True, verbose_name="Usar TLS")

    activa = models.BooleanField(default=True, verbose_name="Configuración activa")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Configuración General"
        verbose_name_plural = "Configuraciones Generales"
        db_table = 'configuracion_general'

    def __str__(self):
        return self.empresa_nombre

    def save(self, *args, **kwargs):
        # Solo puede haber una configuración activa
        if self.activa:
            ConfiguracionGeneral.objects.exclude(pk=self.pk).update(activa=False)
        super().save(*args, **kwargs)
