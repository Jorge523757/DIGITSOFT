from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from inventario.models import Producto
from administrador.models import Administrador


class Carrito(models.Model):
    """Modelo para gestión de carritos de compra"""
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
        return self.precio_unitario * self.cantidad


class Venta(models.Model):
    """Modelo para gestión de ventas"""
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


class DetalleVenta(models.Model):
    """Detalle de productos vendidos en una venta"""
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles', verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        db_table = 'detalles_venta'

    def __str__(self):
        return f"{self.venta.numero_venta} - {self.producto.nombre} x{self.cantidad}"

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
