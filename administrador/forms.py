from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Tecnico, Marca, Proveedor, Producto, Cliente, Equipo, 
    Compra, Venta, Garantia, ServicioTecnico, 
    OrdenServicio, Carrito, Administrador
)

# ========== FORMULARIO DE PRODUCTO ========== #
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo_producto', 'nombre', 'descripcion', 'categoria',
            'marca', 'modelo', 'proveedor_principal', 'precio_compra',
            'precio_venta', 'stock_actual', 'stock_minimo', 'stock_maximo',
            'ubicacion_almacen', 'imagen', 'garantia_meses'
        ]
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único del producto'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'proveedor_principal': forms.Select(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ubicacion_almacen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A-01-05'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'garantia_meses': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data.get('precio_venta')
        precio_compra = self.cleaned_data.get('precio_compra')
        
        if precio_compra and precio_venta and precio_venta < precio_compra:
            raise ValidationError('El precio de venta no puede ser menor al precio de compra.')
        
        return precio_venta

    def clean_stock_maximo(self):
        stock_maximo = self.cleaned_data.get('stock_maximo')
        stock_minimo = self.cleaned_data.get('stock_minimo')
        
        if stock_minimo and stock_maximo and stock_maximo < stock_minimo:
            raise ValidationError('El stock máximo no puede ser menor al stock mínimo.')
        
        return stock_maximo


# ========== FORMULARIO DE CLIENTE ========== #
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_documento', 'numero_documento', 'nombres', 'apellidos',
            'razon_social', 'tipo_cliente', 'telefono', 'email',
            'direccion', 'ciudad', 'departamento'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres completos'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo para empresas'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance_id = self.instance.id if self.instance else None
        
        if Cliente.objects.filter(email=email).exclude(id=instance_id).exists():
            raise ValidationError('Ya existe un cliente con este correo electrónico.')
        
        return email

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        instance_id = self.instance.id if self.instance else None
        
        if Cliente.objects.filter(numero_documento=numero_documento).exclude(id=instance_id).exists():
            raise ValidationError('Ya existe un cliente con este número de documento.')
        
        return numero_documento


# ========== FORMULARIO DE PROVEEDOR ========== #
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'tipo_documento', 'numero_documento', 'razon_social', 'nombre_comercial',
            'telefono', 'email', 'sitio_web', 'direccion', 'ciudad', 'departamento',
            'categoria_principal', 'contacto_principal', 'telefono_contacto', 
            'email_contacto', 'condiciones_pago', 'tiempo_entrega_dias'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT o documento'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón social'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre comercial'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono principal'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@proveedor.com'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_principal': forms.Select(attrs={'class': 'form-control'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del contacto'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono contacto'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email contacto'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tiempo_entrega_dias': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        instance_id = self.instance.id if self.instance else None
        
        if Proveedor.objects.filter(email=email).exclude(id=instance_id).exists():
            raise ValidationError('Ya existe un proveedor con este correo electrónico.')
        
        return email


# ========== FORMULARIO DE MARCA ========== #
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'tipo_marca', 'descripcion', 'pais_origen', 'sitio_web', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
            'tipo_marca': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pais_origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País de origen'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.marca.com'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        instance_id = self.instance.id if self.instance else None
        
        if Marca.objects.filter(nombre__iexact=nombre).exclude(id=instance_id).exists():
            raise ValidationError('Ya existe una marca con este nombre.')
        
        return nombre


# ========== FORMULARIO DE EQUIPO ========== #
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'codigo_equipo', 'nombre', 'cliente', 'tipo_equipo', 'marca',
            'modelo', 'serial', 'estado_fisico', 'especificaciones'
        ]
        widgets = {
            'codigo_equipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del equipo'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_equipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'estado_fisico': forms.Select(attrs={'class': 'form-control'}),
            'especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ========== FORMULARIO DE TÉCNICO ========== #
class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = [
            'numero_documento', 'nombres', 'apellidos', 'telefono', 'email',
            'especialidades', 'nivel_experiencia', 'certificaciones'
        ]
        widgets = {
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'especialidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-control'}),
            'certificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ========== FORMULARIO DE ORDEN DE SERVICIO ========== #
class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = [
            'cliente', 'equipo', 'descripcion_problema',
            'tecnico_asignado', 'prioridad', 'fecha_estimada_entrega'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tecnico_asignado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'fecha_estimada_entrega': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


# ========== FORMULARIO DE VENTA ========== #
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ========== FORMULARIO DE COMPRA ========== #
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'metodo_pago', 'observaciones']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ========== FORMULARIO DE GARANTÍA ========== #
class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = [
            'producto', 'equipo', 'venta', 'cliente', 'fecha_inicio',
            'fecha_vencimiento', 'duracion_meses', 'tipo_garantia', 'cobertura', 'condiciones'
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'equipo': forms.Select(attrs={'class': 'form-control'}),
            'venta': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duracion_meses': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'tipo_garantia': forms.Select(attrs={'class': 'form-control'}),
            'cobertura': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ========== FORMULARIO DE SERVICIO TÉCNICO (CATÁLOGO) ========== #
class ServicioTecnicoForm(forms.ModelForm):
    class Meta:
        model = ServicioTecnico
        fields = [
            'nombre', 'codigo', 'descripcion', 'categoria',
            'precio_base', 'tiempo_estimado_horas', 'requiere_materiales',
            'especificaciones', 'garantia_dias'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'tiempo_estimado_horas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'requiere_materiales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'garantia_dias': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
