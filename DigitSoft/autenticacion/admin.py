from django.contrib import admin
from .models import PerfilUsuario, TokenRecuperacion, HistorialAcceso

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_usuario', 'documento', 'telefono', 'estado', 'fecha_creacion']
    list_filter = ['tipo_usuario', 'estado', 'puede_crear_usuarios']
    search_fields = ['user__username', 'user__email', 'documento', 'user__first_name', 'user__last_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'tipo_usuario', 'estado')
        }),
        ('Datos Personales', {
            'fields': ('documento', 'telefono', 'direccion')
        }),
        ('Permisos', {
            'fields': ('puede_crear_usuarios',)
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TokenRecuperacion)
class TokenRecuperacionAdmin(admin.ModelAdmin):
    list_display = ['user', 'codigo', 'fecha_creacion', 'fecha_expiracion', 'usado']
    list_filter = ['usado', 'fecha_creacion']
    search_fields = ['user__username', 'user__email', 'codigo']
    readonly_fields = ['token', 'codigo', 'fecha_creacion']

@admin.register(HistorialAcceso)
class HistorialAccesoAdmin(admin.ModelAdmin):
    list_display = ['username', 'tipo_accion', 'ip_address', 'exitoso', 'fecha']
    list_filter = ['tipo_accion', 'exitoso', 'fecha']
    search_fields = ['username', 'ip_address', 'mensaje']
    readonly_fields = ['user', 'tipo_accion', 'username', 'ip_address', 'user_agent', 'exitoso', 'mensaje', 'fecha']
    date_hierarchy = 'fecha'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

