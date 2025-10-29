from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from inventario.models import Equipo
from compras.models import Tecnico


class ServicioTecnico(models.Model):
    """Modelo para catálogo de servicios técnicos"""
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


class OrdenServicio(models.Model):
    """Modelo para órdenes de servicio técnico"""
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
