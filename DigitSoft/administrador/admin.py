"""
DigitSoft - Módulo de Administrador
Admin

Configuración del panel de administración para el módulo de administrador.

Autor: DigitSoft Development Team
Fecha: Octubre 2025
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Administrador, LogActividad, ConfiguracionGeneral

# ========== ADMINISTRADOR ========== #
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['user', 'cargo', 'departamento', 'fecha_ingreso', 'activo']
    list_filter = ['activo', 'departamento', 'fecha_ingreso']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'cargo']
    readonly_fields = ['user']

    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('telefono', 'cargo', 'departamento')
        }),
        ('Información Laboral', {
            'fields': ('fecha_ingreso', 'activo')
        }),
    )


# ========== LOG DE ACTIVIDADES ========== #
@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ['administrador', 'tipo_actividad', 'modulo_afectado', 'fecha_actividad', 'ip_address']
    list_filter = ['tipo_actividad', 'modulo_afectado', 'fecha_actividad']
    search_fields = ['administrador__user__username', 'descripcion', 'ip_address']
    readonly_fields = ['administrador', 'tipo_actividad', 'descripcion', 'modulo_afectado',
                      'registro_afectado_id', 'ip_address', 'user_agent', 'fecha_actividad']

    def has_add_permission(self, request):
        # No permitir agregar logs manualmente
        return False

    def has_change_permission(self, request, obj=None):
        # No permitir editar logs
        return False

    def has_delete_permission(self, request, obj=None):
        # Solo permitir eliminar a superusuarios
        return request.user.is_superuser


# ========== CONFIGURACIÓN GENERAL ========== #
@admin.register(ConfiguracionGeneral)
class ConfiguracionGeneralAdmin(admin.ModelAdmin):
    list_display = ['empresa_nombre', 'empresa_nit', 'activa', 'fecha_actualizacion']
    list_filter = ['activa']
    search_fields = ['empresa_nombre', 'empresa_nit']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('empresa_nombre', 'empresa_nit', 'empresa_direccion',
                      'empresa_telefono', 'empresa_email', 'empresa_logo')
        }),
        ('Configuración Financiera', {
            'fields': ('iva_porcentaje', 'moneda', 'timezone')
        }),
        ('Facturación Electrónica', {
            'fields': ('resolucion_dian', 'rango_numeracion_desde',
                      'rango_numeracion_hasta', 'prefijo_factura')
        }),
        ('Configuración de Email', {
            'fields': ('email_smtp_server', 'email_smtp_port', 'email_username',
                      'email_password', 'email_use_tls'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activa', 'fecha_registro', 'fecha_actualizacion')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar configuraciones
        return False

