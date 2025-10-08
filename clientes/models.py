from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Cliente(models.Model):
    """Modelo para gestión de clientes"""
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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Usuario del sistema"
    )

    tipo_documento = models.CharField(
        max_length=3,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de documento"
    )
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de documento"
    )
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Apellidos"
    )
    razon_social = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Razón social"
    )
    tipo_cliente = models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE_CHOICES,
        default='NATURAL',
        verbose_name="Tipo de cliente"
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
