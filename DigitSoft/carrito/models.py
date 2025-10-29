from django.db import models
from django.utils import timezone

# Create your models here.

class Carrito(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('ABANDONADO', 'Abandonado'),
        ('CONVERTIDO', 'Convertido a Venta'),
        ('EXPIRADO', 'Expirado'),
    ]

    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, verbose_name="Cliente")
    codigo_sesion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Código de sesión")

    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    total_items = models.PositiveIntegerField(default=0, verbose_name="Total de items")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Subtotal")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    fecha_expiracion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de expiración")

    # Relación con venta si se convierte
    venta_generada = models.OneToOneField('venta.Venta', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Venta generada")

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

    @property
    def esta_expirado(self):
        return timezone.now() > self.fecha_expiracion

    @property
    def puede_convertir_venta(self):
        return self.estado == 'ACTIVO' and self.total_items > 0 and not self.esta_expirado


class ItemCarrito(models.Model):
    """Modelo para los items del carrito"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', verbose_name="Carrito")
    equipo = models.ForeignKey('equipo.Equipo', on_delete=models.CASCADE, verbose_name="Equipo")

    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha agregado")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")

    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"
        db_table = 'items_carrito'
        unique_together = ['carrito', 'equipo']

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar totales del carrito padre
        self.carrito.actualizar_totales()

    def delete(self, *args, **kwargs):
        carrito = self.carrito
        super().delete(*args, **kwargs)
        # Actualizar totales del carrito padre después de eliminar
        carrito.actualizar_totales()

    def __str__(self):
        return f"{self.carrito} - {self.equipo} (x{self.cantidad})"
