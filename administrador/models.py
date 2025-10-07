from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

# ========== MODELOS CONSOLIDADOS - DIGIT SOFT ========== #

# ========== ADMINISTRADOR ========== #
class Administrador(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]

    ROL_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('SUPERVISOR', 'Supervisor'),
        ('CONTADOR', 'Contador'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
        ('VACACIONES', 'De Vacaciones'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario del sistema")
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de documento")
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")

    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(validators=[telefono_validator], max_length=17, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    direccion = models.TextField(verbose_name="Dirección")

    rol = models.CharField(max_length=15, choices=ROL_CHOICES, verbose_name="Rol")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario")

    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")

    # Permisos específicos
    puede_aprobar_compras = models.BooleanField(default=False, verbose_name="Puede aprobar compras")
    puede_anular_facturas = models.BooleanField(default=False, verbose_name="Puede anular facturas")
    puede_modificar_precios = models.BooleanField(default=False, verbose_name="Puede modificar precios")
    puede_ver_reportes_financieros = models.BooleanField(default=False, verbose_name="Puede ver reportes financieros")
    puede_gestionar_usuarios = models.BooleanField(default=False, verbose_name="Puede gestionar usuarios")

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        ordering = ['apellidos', 'nombres']
        db_table = 'administradores'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.get_rol_display()}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def esta_activo(self):
        return self.estado == 'ACTIVO' and self.user.is_active


# ========== CLIENTES ========== #
class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    ]

    TIPO_CLIENTE_CHOICES = [
        ('NATURAL', 'Persona Natural'),
        ('JURIDICA', 'Persona Jurídica'),
    ]

    # Relación con el usuario del sistema
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario del sistema")

    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de documento")
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, blank=True, null=True, verbose_name="Apellidos")
    razon_social = models.CharField(max_length=200, blank=True, null=True, verbose_name="Razón social")
    tipo_cliente = models.CharField(max_length=10, choices=TIPO_CLIENTE_CHOICES, default='NATURAL', verbose_name="Tipo de cliente")

    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(validators=[telefono_validator], max_length=17, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")

    activo = models.BooleanField(default=True, verbose_name="Cliente activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombres', 'apellidos']
        db_table = 'clientes'

    def __str__(self):
        if self.tipo_cliente == 'JURIDICA':
            return f"{self.razon_social} - {self.numero_documento}"
        return f"{self.nombres} {self.apellidos or ''} - {self.numero_documento}".strip()

    @property
    def nombre_completo(self):
        if self.tipo_cliente == 'JURIDICA':
            return self.razon_social
        return f"{self.nombres} {self.apellidos or ''}".strip()


# ========== TÉCNICOS ========== #
class Tecnico(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]

    NIVEL_EXPERIENCIA_CHOICES = [
        ('JUNIOR', 'Junior'),
        ('INTERMEDIO', 'Intermedio'),
        ('SENIOR', 'Senior'),
        ('ESPECIALISTA', 'Especialista'),
    ]

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADO', 'Ocupado'),
        ('DESCANSO', 'En descanso'),
        ('VACACIONES', 'De vacaciones'),
        ('INCAPACITADO', 'Incapacitado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario del sistema")
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de documento")
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")

    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(validators=[telefono_validator], max_length=17, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    direccion = models.TextField(verbose_name="Dirección")

    especialidades = models.TextField(verbose_name="Especialidades técnicas")
    nivel_experiencia = models.CharField(max_length=12, choices=NIVEL_EXPERIENCIA_CHOICES, verbose_name="Nivel de experiencia")
    certificaciones = models.TextField(blank=True, null=True, verbose_name="Certificaciones")
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salario")

    estado_actual = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='DISPONIBLE', verbose_name="Estado actual")
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Calificación promedio")
    servicios_completados = models.PositiveIntegerField(default=0, verbose_name="Servicios completados")

    activo = models.BooleanField(default=True, verbose_name="Técnico activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
        ordering = ['apellidos', 'nombres']
        db_table = 'tecnicos'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_documento}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def esta_disponible(self):
        return self.estado_actual == 'DISPONIBLE' and self.activo


# ========== MARCAS ========== #
class Marca(models.Model):
    TIPO_MARCA_CHOICES = [
        ('EQUIPOS', 'Equipos de Cómputo'),
        ('COMPONENTES', 'Componentes'),
        ('SOFTWARE', 'Software'),
        ('ACCESORIOS', 'Accesorios'),
        ('CONSUMIBLES', 'Consumibles'),
    ]

    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la marca")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    tipo_marca = models.CharField(max_length=12, choices=TIPO_MARCA_CHOICES, verbose_name="Tipo de marca")
    pais_origen = models.CharField(max_length=100, blank=True, null=True, verbose_name="País de origen")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio web oficial")
    logo = models.ImageField(upload_to='marcas/logos/', blank=True, null=True, verbose_name="Logo")

    activa = models.BooleanField(default=True, verbose_name="Marca activa")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nombre']
        db_table = 'marcas'

    def __str__(self):
        return self.nombre


# ========== PROVEEDORES ========== #
class Proveedor(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('NIT', 'NIT'),
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
    ]

    CATEGORIA_CHOICES = [
        ('EQUIPOS', 'Equipos de Cómputo'),
        ('COMPONENTES', 'Componentes y Partes'),
        ('SOFTWARE', 'Software y Licencias'),
        ('ACCESORIOS', 'Accesorios'),
        ('CONSUMIBLES', 'Consumibles'),
        ('SERVICIOS', 'Servicios'),
    ]

    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default='NIT', verbose_name="Tipo de documento")
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    razon_social = models.CharField(max_length=200, verbose_name="Razón social")
    nombre_comercial = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nombre comercial")

    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(validators=[telefono_validator], max_length=17, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio web")

    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    pais = models.CharField(max_length=100, default='Colombia', verbose_name="País")

    categoria_principal = models.CharField(max_length=15, choices=CATEGORIA_CHOICES, verbose_name="Categoría principal")
    contacto_principal = models.CharField(max_length=100, verbose_name="Contacto principal")
    telefono_contacto = models.CharField(validators=[telefono_validator], max_length=17, blank=True, null=True, verbose_name="Teléfono contacto")
    email_contacto = models.EmailField(blank=True, null=True, verbose_name="Email contacto")

    condiciones_pago = models.TextField(blank=True, null=True, verbose_name="Condiciones de pago")
    tiempo_entrega_dias = models.PositiveIntegerField(default=1, verbose_name="Tiempo de entrega (días)")
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Calificación")

    activo = models.BooleanField(default=True, verbose_name="Proveedor activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['razon_social']
        db_table = 'proveedores'

    def __str__(self):
        return self.razon_social or self.nombre_comercial


# ========== PRODUCTOS ========== #
class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('HARDWARE', 'Hardware'),
        ('SOFTWARE', 'Software'),
        ('ACCESORIOS', 'Accesorios'),
        ('CONSUMIBLES', 'Consumibles'),
        ('COMPONENTES', 'Componentes'),
        ('SERVICIOS', 'Servicios'),
    ]

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('AGOTADO', 'Agotado'),
        ('DESCONTINUADO', 'Descontinuado'),
        ('PROXIMAMENTE', 'Próximamente'),
    ]

    codigo_producto = models.CharField(max_length=20, unique=True, verbose_name="Código del producto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES, verbose_name="Categoría")

    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    modelo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modelo")

    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio de compra")
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio de venta")
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Margen de ganancia (%)")

    stock_actual = models.PositiveIntegerField(default=0, verbose_name="Stock actual")
    stock_minimo = models.PositiveIntegerField(default=1, verbose_name="Stock mínimo")
    stock_maximo = models.PositiveIntegerField(default=100, verbose_name="Stock máximo")

    unidad_medida = models.CharField(max_length=20, default='Unidad', verbose_name="Unidad de medida")
    ubicacion_almacen = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ubicación en almacén")

    proveedor_principal = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Proveedor principal")

    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del producto")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='DISPONIBLE', verbose_name="Estado")

    especificaciones = models.TextField(blank=True, null=True, verbose_name="Especificaciones técnicas")
    garantia_meses = models.PositiveIntegerField(default=12, verbose_name="Garantía (meses)")

    # Campos SEO/Web
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="URL amigable")
    meta_descripcion = models.TextField(blank=True, null=True, max_length=160, verbose_name="Meta descripción")
    palabras_clave = models.CharField(max_length=255, blank=True, null=True, verbose_name="Palabras clave")

    activo = models.BooleanField(default=True, verbose_name="Producto activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
        db_table = 'productos'

    def __str__(self):
        return f"{self.codigo_producto} - {self.nombre}"

    def save(self, *args, **kwargs):
        if not self.codigo_producto:
            # Generar código automático
            fecha = timezone.now().strftime('%Y%m')
            ultimo = Producto.objects.filter(codigo_producto__startswith=f'PRD{fecha}').count()
            self.codigo_producto = f'PRD{fecha}{(ultimo + 1):04d}'

        # Calcular margen de ganancia
        if self.precio_compra and self.precio_venta:
            if self.precio_compra > 0:
                self.margen_ganancia = ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100

        # Generar slug si no existe
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)

    @property
    def precio_con_iva(self):
        # IVA por defecto 19%
        from decimal import Decimal
        return self.precio_venta * Decimal('1.19')

    @property
    def necesita_restock(self):
        return self.stock_actual <= self.stock_minimo


# ========== EQUIPOS ========== #
class Equipo(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('DESKTOP', 'Computador de Escritorio'),
        ('LAPTOP', 'Computador Portátil'),
        ('SERVER', 'Servidor'),
        ('PRINTER', 'Impresora'),
        ('SCANNER', 'Escáner'),
        ('NETWORK', 'Equipo de Red'),
        ('MONITOR', 'Monitor'),
        ('UPS', 'UPS'),
        ('OTROS', 'Otros'),
    ]

    ESTADO_CHOICES = [
        ('NUEVO', 'Nuevo'),
        ('BUENO', 'Bueno'),
        ('REGULAR', 'Regular'),
        ('MALO', 'Malo'),
        ('DAÑADO', 'Dañado'),
        ('EN_REPARACION', 'En Reparación'),
    ]

    codigo_equipo = models.CharField(max_length=20, unique=True, verbose_name="Código del equipo")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del equipo")
    tipo_equipo = models.CharField(max_length=10, choices=TIPO_EQUIPO_CHOICES, verbose_name="Tipo de equipo")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    serial = models.CharField(max_length=100, unique=True, verbose_name="Número de serie")

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente propietario")

    fecha_compra = models.DateField(blank=True, null=True, verbose_name="Fecha de compra")
    valor_compra = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Valor de compra")
    estado_fisico = models.CharField(max_length=15, choices=ESTADO_CHOICES, verbose_name="Estado físico")

    especificaciones = models.TextField(verbose_name="Especificaciones técnicas")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    activo = models.BooleanField(default=True, verbose_name="Equipo activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ['codigo_equipo']
        db_table = 'equipos'

    def __str__(self):
        return f"{self.codigo_equipo} - {self.nombre}"


# ========== SERVICIOS TÉCNICOS ========== #
class ServicioTecnico(models.Model):
    CATEGORIA_CHOICES = [
        ('HARDWARE', 'Hardware'),
        ('SOFTWARE', 'Software'),
        ('REDES', 'Redes'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('INSTALACION', 'Instalación'),
        ('CONSULTORIA', 'Consultoría'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre del servicio")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del servicio")
    descripcion = models.TextField(verbose_name="Descripción del servicio")
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES, verbose_name="Categoría")

    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio base")
    tiempo_estimado_horas = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tiempo estimado (horas)")
    requiere_materiales = models.BooleanField(default=False, verbose_name="Requiere materiales")

    especificaciones = models.TextField(blank=True, null=True, verbose_name="Especificaciones técnicas")
    herramientas_requeridas = models.TextField(blank=True, null=True, verbose_name="Herramientas requeridas")
    prerequisitos = models.TextField(blank=True, null=True, verbose_name="Prerequisitos")

    garantia_dias = models.PositiveIntegerField(default=30, verbose_name="Garantía (días)")
    activo = models.BooleanField(default=True, verbose_name="Servicio activo")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Servicio Técnico"
        verbose_name_plural = "Servicios Técnicos"
        ordering = ['categoria', 'nombre']
        db_table = 'servicios_tecnicos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


# ========== ÓRDENES DE SERVICIO ========== #
class OrdenServicio(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('PAUSADA', 'Pausada'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('FACTURADA', 'Facturada'),
    ]

    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    numero_orden = models.CharField(max_length=20, unique=True, verbose_name="Número de orden")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")
    tecnico_asignado = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Técnico asignado")

    descripcion_problema = models.TextField(verbose_name="Descripción del problema")
    diagnostico = models.TextField(blank=True, null=True, verbose_name="Diagnóstico técnico")
    solucion_aplicada = models.TextField(blank=True, null=True, verbose_name="Solución aplicada")

    fecha_ingreso = models.DateTimeField(default=timezone.now, verbose_name="Fecha de ingreso")
    fecha_estimada_entrega = models.DateTimeField(blank=True, null=True, verbose_name="Fecha estimada de entrega")
    fecha_entrega_real = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de entrega real")

    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")
    prioridad = models.CharField(max_length=8, choices=PRIORIDAD_CHOICES, default='MEDIA', verbose_name="Prioridad")

    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo mano de obra")
    costo_repuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo repuestos")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total")

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Orden de Servicio"
        verbose_name_plural = "Órdenes de Servicio"
        ordering = ['-fecha_ingreso']
        db_table = 'ordenes_servicio'

    def __str__(self):
        return f"{self.numero_orden} - {self.cliente}"


# ========== COMPRAS ========== #
class Compra(models.Model):
    ESTADO_CHOICES = [
        ('SOLICITUD', 'Solicitud'),
        ('COTIZACION', 'Cotización'),
        ('APROBADA', 'Aprobada'),
        ('PEDIDO_ENVIADO', 'Pedido Enviado'),
        ('RECIBIDA_PARCIAL', 'Recibida Parcial'),
        ('RECIBIDA_COMPLETA', 'Recibida Completa'),
        ('FACTURADA', 'Facturada'),
        ('PAGADA', 'Pagada'),
        ('CANCELADA', 'Cancelada'),
    ]

    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
        ('TARJETA_CREDITO', 'Tarjeta de Crédito'),
    ]

    numero_compra = models.CharField(max_length=20, unique=True, verbose_name="Número de compra")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name="Proveedor")
    solicitado_por = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Solicitado por")

    fecha_solicitud = models.DateTimeField(default=timezone.now, verbose_name="Fecha de solicitud")
    fecha_cotizacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de cotización")
    fecha_aprobacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de aprobación")
    fecha_pedido = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de pedido")
    fecha_entrega_estimada = models.DateTimeField(blank=True, null=True, verbose_name="Fecha entrega estimada")
    fecha_entrega_real = models.DateTimeField(blank=True, null=True, verbose_name="Fecha entrega real")

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='SOLICITUD', verbose_name="Estado")

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Subtotal")
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Descuento")
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Impuestos")
    costos_envio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Costos de envío")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total")

    metodo_pago = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES, blank=True, null=True, verbose_name="Método de pago")
    numero_factura_proveedor = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número factura proveedor")

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    condiciones_pago = models.TextField(blank=True, null=True, verbose_name="Condiciones de pago")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha_solicitud']
        db_table = 'compras'

    def __str__(self):
        return f"{self.numero_compra} - {self.proveedor}"

    def save(self, *args, **kwargs):
        if not self.numero_compra:
            # Generar número de compra automático
            fecha = timezone.now().strftime('%Y%m')
            ultimo = Compra.objects.filter(numero_compra__startswith=f'C{fecha}').count()
            self.numero_compra = f'C{fecha}{(ultimo + 1):04d}'

        # Calcular total
        self.total = self.subtotal - self.descuento + self.impuestos + self.costos_envio
        super().save(*args, **kwargs)

    @property
    def total_productos(self):
        """Retorna el total de productos en la compra"""
        # Comentado temporalmente hasta crear el modelo DetalleCompra
        # return self.detallecompra_set.aggregate(
        #     total=models.Sum('cantidad')
        # )['total'] or 0
        return 0


# ========== CARRITOS ========== #
class Carrito(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('ABANDONADO', 'Abandonado'),
        ('CONVERTIDO', 'Convertido a Venta'),
        ('EXPIRADO', 'Expirado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    codigo_sesion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Código de sesión")

    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    total_items = models.PositiveIntegerField(default=0, verbose_name="Total de items")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Subtotal")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    fecha_expiracion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de expiración")

    # Relación con venta si se convierte
    venta_generada = models.OneToOneField('Venta', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Venta generada")

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        ordering = ['-fecha_actualizacion']
        db_table = 'carritos'

    def __str__(self):
        return f"Carrito {self.id} - {self.cliente} ({self.total_items} items)"

    def save(self, *args, **kwargs):
        # Establecer fecha de expiración si no existe (7 días por defecto)
        if not self.fecha_expiracion:
            from datetime import timedelta
            self.fecha_expiracion = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def actualizar_totales(self):
        """Actualizar totales del carrito basado en los items"""
        items = self.items.all()
        self.total_items = sum(item.cantidad for item in items)
        self.subtotal = sum(item.subtotal for item in items)
        self.save()


# ========== ITEMS DEL CARRITO ========== #
class ItemCarrito(models.Model):
    """Items individuales dentro de un carrito de compras"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', verbose_name="Carrito")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")

    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha agregado")

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        db_table = 'items_carrito'
        unique_together = ['carrito', 'producto']

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad} - Carrito #{self.carrito.id}"

    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.precio_unitario * self.cantidad


# ========== VENTAS ========== #
class Venta(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('PARCIAL', 'Pago Parcial'),
        ('ANULADA', 'Anulada'),
        ('CREDITO', 'A Crédito'),
    ]

    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_DEBITO', 'Tarjeta Débito'),
        ('TARJETA_CREDITO', 'Tarjeta Crédito'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CREDITO', 'A Crédito'),
        ('MIXTO', 'Mixto'),
    ]

    numero_venta = models.CharField(max_length=20, unique=True, verbose_name="Número de venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name="Cliente")
    vendedor = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, verbose_name="Vendedor")

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Descuento")
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Impuestos")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")

    metodo_pago = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES, verbose_name="Método de pago")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")

    fecha_venta = models.DateTimeField(default=timezone.now, verbose_name="Fecha de venta")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']
        db_table = 'ventas'

    def __str__(self):
        return f"{self.numero_venta} - {self.cliente}"


# ========== GARANTÍAS ========== #
class Garantia(models.Model):
    ESTADO_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('VENCIDA', 'Vencida'),
        ('RECLAMADA', 'Reclamada'),
        ('PROCESANDO', 'Procesando'),
        ('RECHAZADA', 'Rechazada'),
    ]

    TIPO_GARANTIA_CHOICES = [
        ('FABRICANTE', 'Garantía del Fabricante'),
        ('DISTRIBUIDOR', 'Garantía del Distribuidor'),
        ('TIENDA', 'Garantía de la Tienda'),
        ('EXTENDIDA', 'Garantía Extendida'),
    ]

    numero_garantia = models.CharField(max_length=20, unique=True, verbose_name="Número de garantía")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Producto")
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Equipo")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Venta relacionada")

    tipo_garantia = models.CharField(max_length=12, choices=TIPO_GARANTIA_CHOICES, verbose_name="Tipo de garantía")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    duracion_meses = models.PositiveIntegerField(verbose_name="Duración en meses")

    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='VIGENTE', verbose_name="Estado")

    condiciones = models.TextField(blank=True, null=True, verbose_name="Condiciones de la garantía")
    cobertura = models.TextField(blank=True, null=True, verbose_name="Cobertura")
    exclusiones = models.TextField(blank=True, null=True, verbose_name="Exclusiones")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        ordering = ['-fecha_inicio']
        db_table = 'garantias'

    def __str__(self):
        return f"{self.numero_garantia} - {self.cliente}"

    @property
    def esta_vigente(self):
        from datetime import date
        return self.fecha_vencimiento >= date.today() and self.estado == 'VIGENTE'


# ========== FACTURACIÓN ========== #
class Factura(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('EMITIDA', 'Emitida'),
        ('PAGADA', 'Pagada'),
        ('VENCIDA', 'Vencida'),
        ('ANULADA', 'Anulada'),
    ]

    TIPO_FACTURA_CHOICES = [
        ('VENTA', 'Venta'),
        ('SERVICIO', 'Servicio'),
        ('MIXTA', 'Mixta'),
    ]

    numero_factura = models.CharField(max_length=20, unique=True, verbose_name="Número de factura")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name="Cliente")
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Venta relacionada")
    orden_servicio = models.OneToOneField(OrdenServicio, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Orden de servicio")

    tipo_factura = models.CharField(max_length=8, choices=TIPO_FACTURA_CHOICES, verbose_name="Tipo de factura")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='BORRADOR', verbose_name="Estado")

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Descuento")
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Impuestos")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")

    fecha_emision = models.DateTimeField(default=timezone.now, verbose_name="Fecha de emisión")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_emision']
        db_table = 'facturas'

    def __str__(self):
        return f"{self.numero_factura} - {self.cliente}"


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
