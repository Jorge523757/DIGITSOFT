from django.db import models

# Create your models here.

class Notificacion(models.Model):
    """Modelo para notificaciones del sistema"""
    TIPO_CHOICES = [
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Éxito'),
    ]

    CATEGORIA_CHOICES = [
        ('SISTEMA', 'Sistema'),
        ('VENTA', 'Venta'),
        ('SERVICIO', 'Servicio'),
        ('INVENTARIO', 'Inventario'),
        ('FACTURACION', 'Facturación'),
        ('GARANTIA', 'Garantía'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES, verbose_name="Categoría")

    # Destinatarios
    para_administradores = models.BooleanField(default=False, verbose_name="Para administradores")
    para_tecnicos = models.BooleanField(default=False, verbose_name="Para técnicos")
    usuario_especifico = models.ForeignKey('administrador.Administrador', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario específico")

    leida = models.BooleanField(default=False, verbose_name="Leída")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_lectura = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de lectura")

    # Referencias actualizadas al módulo administrador consolidado
    orden_servicio_ref = models.ForeignKey('administrador.OrdenServicio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Orden servicio referencia")
    venta_ref = models.ForeignKey('administrador.Venta', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Venta referencia")
    factura_ref = models.ForeignKey('administrador.Factura', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Factura referencia")

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
        db_table = 'notificaciones'

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"

    def marcar_como_leida(self):
        from django.utils import timezone
        self.leida = True
        self.fecha_lectura = timezone.now()
        self.save()


class HistorialCambios(models.Model):
    """Modelo para registrar cambios en registros importantes"""
    tabla_afectada = models.CharField(max_length=100, verbose_name="Tabla afectada")
    registro_id = models.PositiveIntegerField(verbose_name="ID del registro")
    campo_modificado = models.CharField(max_length=100, verbose_name="Campo modificado")
    valor_anterior = models.TextField(blank=True, null=True, verbose_name="Valor anterior")
    valor_nuevo = models.TextField(blank=True, null=True, verbose_name="Valor nuevo")

    usuario = models.ForeignKey('administrador.Administrador', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Usuario que realizó el cambio")
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del cambio")
    razon_cambio = models.TextField(blank=True, null=True, verbose_name="Razón del cambio")

    class Meta:
        verbose_name = "Historial de Cambios"
        verbose_name_plural = "Historial de Cambios"
        ordering = ['-fecha_cambio']
        db_table = 'historial_cambios'

    def __str__(self):
        return f"{self.tabla_afectada} #{self.registro_id} - {self.campo_modificado} - {self.fecha_cambio}"
