from django.db import models
from django.utils import timezone
from clientes.models import Cliente


class Marca(models.Model):
    """Modelo para gestión de marcas"""
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


class Producto(models.Model):
    """Modelo para gestión de productos"""
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

    proveedor_principal = models.ForeignKey(
        'proveedores.Proveedor',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Proveedor principal"
    )

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


class Equipo(models.Model):
    """Modelo para gestión de equipos de clientes"""
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
