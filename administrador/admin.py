from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Administrador, Cliente, Tecnico, Marca, Proveedor, Producto,
    Equipo, ServicioTecnico, OrdenServicio, Compra, Carrito,
    Venta, Garantia, Factura, LogActividad, ConfiguracionGeneral
)

# ========== ADMINISTRADOR ========== #
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'nombre_completo', 'email', 'rol', 'estado', 'fecha_ingreso']
    list_filter = ['rol', 'estado', 'departamento']
    search_fields = ['numero_documento', 'nombres', 'apellidos', 'email']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('user', 'tipo_documento', 'numero_documento', 'nombres', 'apellidos')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Laboral', {
            'fields': ('rol', 'departamento', 'fecha_ingreso', 'salario', 'estado')
        }),
        ('Permisos', {
            'fields': ('puede_aprobar_compras', 'puede_anular_facturas', 'puede_modificar_precios',
                      'puede_ver_reportes_financieros', 'puede_gestionar_usuarios')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========== CLIENTES ========== #
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'nombre_completo', 'tipo_cliente', 'email', 'ciudad', 'activo']
    list_filter = ['tipo_cliente', 'activo', 'ciudad', 'departamento']
    search_fields = ['numero_documento', 'nombres', 'apellidos', 'razon_social', 'email']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información Básica', {
            'fields': ('tipo_documento', 'numero_documento', 'tipo_cliente')
        }),
        ('Datos Personales / Empresa', {
            'fields': ('nombres', 'apellidos', 'razon_social')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'ciudad', 'departamento')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========== TÉCNICOS ========== #
@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'nombre_completo', 'nivel_experiencia', 'estado_actual', 'calificacion_promedio', 'servicios_completados']
    list_filter = ['nivel_experiencia', 'estado_actual', 'activo']
    search_fields = ['numero_documento', 'nombres', 'apellidos', 'especialidades']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información Personal', {
            'fields': ('user', 'tipo_documento', 'numero_documento', 'nombres', 'apellidos')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Información Profesional', {
            'fields': ('especialidades', 'nivel_experiencia', 'certificaciones', 'fecha_ingreso', 'salario')
        }),
        ('Estado y Desempeño', {
            'fields': ('estado_actual', 'calificacion_promedio', 'servicios_completados', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========== MARCAS ========== #
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_marca', 'pais_origen', 'ver_logo', 'activa']
    list_filter = ['tipo_marca', 'activa', 'pais_origen']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'preview_logo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'tipo_marca', 'pais_origen', 'sitio_web')
        }),
        ('Logo', {
            'fields': ('logo', 'preview_logo')
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def ver_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 5px;" />', obj.logo.url)
        return format_html('<div style="width:50px;height:50px;background:#ddd;border-radius:5px;display:flex;align-items:center;justify-content:center;">📷</div>')
    ver_logo.short_description = 'Logo'
    
    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain; border: 2px solid #ddd; border-radius: 8px; padding: 5px;" />', obj.logo.url)
        return format_html('<div style="padding:20px;background:#f0f0f0;border-radius:8px;text-align:center;color:#666;">Sin logo cargado</div>')
    preview_logo.short_description = 'Vista Previa del Logo'


# ========== PROVEEDORES ========== #
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'razon_social', 'categoria_principal', 'ciudad', 'calificacion', 'activo'
    ]
    list_filter = ['categoria_principal', 'activo', 'ciudad', 'pais']
    search_fields = ['numero_documento', 'razon_social', 'nombre_comercial', 'email']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información Empresarial', {
            'fields': ('tipo_documento', 'numero_documento', 'razon_social', 'nombre_comercial', 'categoria_principal')
        }),
        ('Contacto Principal', {
            'fields': ('telefono', 'email', 'sitio_web')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad', 'departamento', 'pais')
        }),
        ('Persona de Contacto', {
            'fields': ('contacto_principal', 'telefono_contacto', 'email_contacto')
        }),
        ('Condiciones Comerciales', {
            'fields': ('condiciones_pago', 'tiempo_entrega_dias', 'calificacion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========== PRODUCTOS ========== #
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo_producto', 'nombre', 'ver_imagen', 'marca', 'categoria', 'precio_venta', 'stock_actual', 'estado', 'activo']
    list_filter = ['categoria', 'estado', 'activo', 'marca']
    search_fields = ['codigo_producto', 'nombre', 'descripcion']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'margen_ganancia', 'preview_imagen', 'codigo_producto']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_producto', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'precio_venta', 'margen_ganancia')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo', 'stock_maximo', 'unidad_medida', 'ubicacion_almacen')
        }),
        ('Proveedor', {
            'fields': ('proveedor_principal',)
        }),
        ('Multimedia', {
            'fields': ('imagen', 'preview_imagen')
        }),
        ('Detalles', {
            'fields': ('especificaciones', 'garantia_meses', 'estado', 'activo')
        }),
        ('SEO/Web', {
            'fields': ('slug', 'meta_descripcion', 'palabras_clave'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def ver_imagen(self, obj):
        """Miniatura en la lista"""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px; border: 1px solid #ddd;" />',
                obj.imagen.url
            )
        return format_html(
            '<div style="width:60px;height:60px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);'
            'border-radius:5px;display:flex;align-items:center;justify-content:center;color:white;font-size:24px;">📦</div>'
        )
    ver_imagen.short_description = 'Imagen'
    
    def preview_imagen(self, obj):
        """Vista previa grande en el formulario"""
        if obj.imagen:
            return format_html(
                '<div style="margin-top: 10px;">'
                '<img src="{}" style="max-width: 400px; max-height: 400px; object-fit: contain; '
                'border: 2px solid #ddd; border-radius: 8px; padding: 5px; background: white;" />'
                '</div>',
                obj.imagen.url
            )
        return format_html(
            '<div style="margin-top: 10px; padding: 40px; background: #f0f0f0; border-radius: 8px; text-align: center;">'
            '<p style="color: #666; font-size: 16px;">📷 No hay imagen cargada</p>'
            '<p style="color: #999; font-size: 12px;">La imagen se mostrará aquí una vez cargada</p>'
            '</div>'
        )
    preview_imagen.short_description = 'Vista Previa de la Imagen'


# ========== EQUIPOS ========== #
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['codigo_equipo', 'nombre', 'tipo_equipo', 'marca', 'get_cliente', 'estado_fisico', 'activo']
    list_filter = ['tipo_equipo', 'estado_fisico', 'activo', 'marca']
    search_fields = ['codigo_equipo', 'nombre', 'serial', 'modelo', 'cliente__nombres', 'cliente__apellidos', 'cliente__razon_social']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'codigo_equipo']
    autocomplete_fields = ['cliente', 'marca']

    fieldsets = (
        ('Información del Equipo', {
            'fields': ('codigo_equipo', 'nombre', 'tipo_equipo', 'marca', 'modelo', 'serial')
        }),
        ('Propietario', {
            'fields': ('cliente',)
        }),
        ('Estado y Valor', {
            'fields': ('estado_fisico', 'fecha_compra', 'valor_compra')
        }),
        ('Especificaciones', {
            'fields': ('especificaciones', 'observaciones')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cliente(self, obj):
        """Mostrar el nombre del cliente"""
        if obj.cliente:
            return format_html(
                '<a href="/admin/administrador/cliente/{}/change/">{}</a>',
                obj.cliente.id,
                obj.cliente.nombre_completo
            )
        return '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'


# ========== SERVICIOS TÉCNICOS ========== #
@admin.register(ServicioTecnico)
class ServicioTecnicoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'precio_base', 'tiempo_estimado_horas', 'activo']
    list_filter = ['categoria', 'activo', 'requiere_materiales']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'categoria')
        }),
        ('Pricing y Tiempo', {
            'fields': ('precio_base', 'tiempo_estimado_horas', 'requiere_materiales')
        }),
        ('Detalles Técnicos', {
            'fields': ('especificaciones', 'herramientas_requeridas', 'prerequisitos')
        }),
        ('Garantía', {
            'fields': ('garantia_dias',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


# ========== ÓRDENES DE SERVICIO ========== #
@admin.register(OrdenServicio)
class OrdenServicioAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'get_cliente', 'get_equipo', 'get_tecnico', 'estado', 'prioridad', 'total', 'fecha_ingreso']
    list_filter = ['estado', 'prioridad', 'fecha_ingreso']
    search_fields = ['numero_orden', 'cliente__nombres', 'cliente__apellidos', 'equipo__nombre', 'tecnico_asignado__nombres']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    date_hierarchy = 'fecha_ingreso'
    autocomplete_fields = ['cliente', 'equipo', 'tecnico_asignado']

    fieldsets = (
        ('Información de la Orden', {
            'fields': ('numero_orden', 'cliente', 'equipo', 'tecnico_asignado')
        }),
        ('Problema y Solución', {
            'fields': ('descripcion_problema', 'diagnostico', 'solucion_aplicada')
        }),
        ('Fechas', {
            'fields': ('fecha_ingreso', 'fecha_estimada_entrega', 'fecha_entrega_real')
        }),
        ('Estado y Prioridad', {
            'fields': ('estado', 'prioridad')
        }),
        ('Costos', {
            'fields': ('costo_mano_obra', 'costo_repuestos', 'total')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cliente(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'

    def get_equipo(self, obj):
        return obj.equipo.nombre if obj.equipo else '-'
    get_equipo.short_description = 'Equipo'
    get_equipo.admin_order_field = 'equipo__nombre'

    def get_tecnico(self, obj):
        return obj.tecnico_asignado.nombre_completo if obj.tecnico_asignado else 'Sin asignar'
    get_tecnico.short_description = 'Técnico'
    get_tecnico.admin_order_field = 'tecnico_asignado__nombres'


# ========== COMPRAS ========== #
@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['numero_compra', 'get_proveedor', 'get_solicitado_por', 'estado', 'total', 'fecha_solicitud']
    list_filter = ['estado', 'metodo_pago', 'fecha_solicitud']
    search_fields = ['numero_compra', 'proveedor__razon_social', 'solicitado_por__nombres']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'numero_compra']
    date_hierarchy = 'fecha_solicitud'
    autocomplete_fields = ['proveedor', 'solicitado_por']

    fieldsets = (
        ('Información de la Compra', {
            'fields': ('numero_compra', 'proveedor', 'solicitado_por', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_cotizacion', 'fecha_aprobacion', 'fecha_pedido',
                      'fecha_entrega_estimada', 'fecha_entrega_real')
        }),
        ('Montos', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'costos_envio', 'total')
        }),
        ('Pago', {
            'fields': ('metodo_pago', 'numero_factura_proveedor', 'condiciones_pago')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_proveedor(self, obj):
        return obj.proveedor.razon_social if obj.proveedor else '-'
    get_proveedor.short_description = 'Proveedor'
    get_proveedor.admin_order_field = 'proveedor__razon_social'

    def get_solicitado_por(self, obj):
        return obj.solicitado_por.nombre_completo if obj.solicitado_por else 'N/A'
    get_solicitado_por.short_description = 'Solicitado por'
    get_solicitado_por.admin_order_field = 'solicitado_por__nombres'


# ========== CARRITOS ========== #
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_cliente', 'estado', 'total_items', 'subtotal', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'codigo_sesion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['cliente', 'venta_generada']

    fieldsets = (
        ('Información del Carrito', {
            'fields': ('cliente', 'codigo_sesion', 'estado')
        }),
        ('Totales', {
            'fields': ('total_items', 'subtotal')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'fecha_expiracion')
        }),
        ('Conversión', {
            'fields': ('venta_generada',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )

    def get_cliente(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'


# ========== VENTAS ========== #
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_venta', 'get_cliente', 'get_vendedor', 'total', 'metodo_pago', 'estado', 'fecha_venta']
    list_filter = ['estado', 'metodo_pago', 'fecha_venta']
    search_fields = ['numero_venta', 'cliente__nombres', 'cliente__apellidos']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    date_hierarchy = 'fecha_venta'
    autocomplete_fields = ['cliente', 'vendedor']

    fieldsets = (
        ('Información de la Venta', {
            'fields': ('numero_venta', 'cliente', 'vendedor', 'fecha_venta')
        }),
        ('Montos', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total')
        }),
        ('Pago', {
            'fields': ('metodo_pago', 'estado')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cliente(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'

    def get_vendedor(self, obj):
        return obj.vendedor.nombre_completo if obj.vendedor else '-'
    get_vendedor.short_description = 'Vendedor'
    get_vendedor.admin_order_field = 'vendedor__nombres'


# ========== GARANTÍAS ========== #
@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ['numero_garantia', 'get_cliente', 'tipo_garantia', 'fecha_inicio', 'fecha_vencimiento', 'estado', 'esta_vigente']
    list_filter = ['estado', 'tipo_garantia', 'fecha_inicio']
    search_fields = ['numero_garantia', 'cliente__nombres', 'cliente__apellidos']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    autocomplete_fields = ['cliente', 'producto', 'equipo', 'venta']

    fieldsets = (
        ('Información de la Garantía', {
            'fields': ('numero_garantia', 'tipo_garantia', 'cliente')
        }),
        ('Producto/Equipo', {
            'fields': ('producto', 'equipo', 'venta')
        }),
        ('Vigencia', {
            'fields': ('fecha_inicio', 'fecha_vencimiento', 'duracion_meses', 'estado')
        }),
        ('Condiciones', {
            'fields': ('condiciones', 'cobertura', 'exclusiones')
        }),
        ('Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cliente(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'


# ========== FACTURAS ========== #
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'get_cliente', 'tipo_factura', 'total', 'estado', 'fecha_emision']
    list_filter = ['estado', 'tipo_factura', 'fecha_emision']
    search_fields = ['numero_factura', 'cliente__nombres', 'cliente__apellidos']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    date_hierarchy = 'fecha_emision'
    autocomplete_fields = ['cliente', 'venta', 'orden_servicio']

    fieldsets = (
        ('Información de la Factura', {
            'fields': ('numero_factura', 'cliente', 'tipo_factura', 'estado')
        }),
        ('Relacionado con', {
            'fields': ('venta', 'orden_servicio')
        }),
        ('Montos', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_vencimiento')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Registro', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cliente(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'cliente__nombres'


# ========== LOG DE ACTIVIDADES ========== #
@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ['get_administrador', 'tipo_actividad', 'modulo_afectado', 'fecha_actividad']
    list_filter = ['tipo_actividad', 'fecha_actividad', 'modulo_afectado']
    search_fields = ['administrador__nombres', 'administrador__apellidos', 'descripcion', 'modulo_afectado']
    readonly_fields = ['fecha_actividad']
    date_hierarchy = 'fecha_actividad'

    fieldsets = (
        ('Actividad', {
            'fields': ('administrador', 'tipo_actividad', 'descripcion')
        }),
        ('Detalles', {
            'fields': ('modulo_afectado', 'registro_afectado_id')
        }),
        ('Información Técnica', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Fecha', {
            'fields': ('fecha_actividad',)
        }),
    )

    def get_administrador(self, obj):
        return obj.administrador.nombre_completo if obj.administrador else '-'
    get_administrador.short_description = 'Administrador'
    get_administrador.admin_order_field = 'administrador__nombres'


# ========== CONFIGURACIÓN GENERAL ========== #
@admin.register(ConfiguracionGeneral)
class ConfiguracionGeneralAdmin(admin.ModelAdmin):
    list_display = ['empresa_nombre', 'empresa_nit', 'moneda', 'iva_porcentaje', 'activa']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'preview_logo']
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('empresa_nombre', 'empresa_nit', 'empresa_direccion', 'empresa_telefono', 'empresa_email')
        }),
        ('Logo', {
            'fields': ('empresa_logo', 'preview_logo')
        }),
        ('Configuración Regional', {
            'fields': ('iva_porcentaje', 'moneda', 'timezone')
        }),
        ('Facturación Electrónica', {
            'fields': ('resolucion_dian', 'rango_numeracion_desde', 'rango_numeracion_hasta', 'prefijo_factura')
        }),
        ('Configuración de Email', {
            'fields': ('email_smtp_server', 'email_smtp_port', 'email_username', 'email_password', 'email_use_tls'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_logo(self, obj):
        if obj.empresa_logo:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain; border: 2px solid #ddd; border-radius: 8px; padding: 5px;" />',
                obj.empresa_logo.url
            )
        return format_html('<div style="padding:20px;background:#f0f0f0;border-radius:8px;text-align:center;color:#666;">Sin logo cargado</div>')
    preview_logo.short_description = 'Vista Previa del Logo'


# Personalizar el sitio de administración
admin.site.site_header = "Digit Soft - Panel de Administración"
admin.site.site_title = "Digit Soft Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"
