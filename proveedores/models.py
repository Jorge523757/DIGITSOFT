from django.db import models
from django.core.validators import RegexValidator


class Proveedor(models.Model):
    """Modelo para gestión de proveedores"""
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

    tipo_documento = models.CharField(
        max_length=3,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='NIT',
        verbose_name="Tipo de documento"
    )
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de documento"
    )
    razon_social = models.CharField(max_length=200, verbose_name="Razón social")
    nombre_comercial = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nombre comercial"
    )

    telefono_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe tener entre 9 y 15 dígitos."
    )
    telefono = models.CharField(
        validators=[telefono_validator],
        max_length=17,
        verbose_name="Teléfono"
    )
    email = models.EmailField(verbose_name="Correo electrónico")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio web")

    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    pais = models.CharField(max_length=100, default='Colombia', verbose_name="País")

    categoria_principal = models.CharField(
        max_length=15,
        choices=CATEGORIA_CHOICES,
        verbose_name="Categoría principal"
    )
    contacto_principal = models.CharField(max_length=100, verbose_name="Contacto principal")
    telefono_contacto = models.CharField(
        validators=[telefono_validator],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Teléfono contacto"
    )
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
