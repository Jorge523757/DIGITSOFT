from django.db import models
from django.utils import timezone
from proveedores.models import Proveedor
from inventario.models import Producto


class Tecnico(models.Model):
    """Modelo para gestión de técnicos"""
    from django.contrib.auth.models import User
    from django.core.validators import RegexValidator

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


class Compra(models.Model):
    """Modelo para gestión de compras"""
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
            fecha = timezone.now().strftime('%Y%m')
            ultimo = Compra.objects.filter(numero_compra__startswith=f'C{fecha}').count()
            self.numero_compra = f'C{fecha}{(ultimo + 1):04d}'

        self.total = self.subtotal - self.descuento + self.impuestos + self.costos_envio
        super().save(*args, **kwargs)


class DetalleCompra(models.Model):
    """Detalle de productos en una compra"""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles', verbose_name="Compra")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compra"
        db_table = 'detalles_compra'

    def __str__(self):
        return f"{self.compra.numero_compra} - {self.producto.nombre} x{self.cantidad}"

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
