from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Tecnico, Marca, Proveedor,
    Equipo, Compra
)


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'tipo_documento', 'numero_documento', 'razon_social', 'nombre_comercial',
            'telefono', 'email', 'sitio_web', 'direccion', 'ciudad', 'departamento',
            'categoria_principal', 'contacto_principal', 'telefono_contacto', 'email_contacto',
            'condiciones_pago', 'tiempo_entrega_dias'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar widgets y atributos
        self.fields['tipo_documento'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['numero_documento'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Número de identificación (NIT, CC, CE)',
            'required': True
        })
        
        self.fields['razon_social'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Razón social de la empresa',
            'required': True
        })
        
        self.fields['nombre_comercial'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre comercial (opcional)'
        })

        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Número de teléfono principal',
            'required': True
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correo electrónico principal',
            'required': True
        })
        
        self.fields['sitio_web'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'https://www.ejemplo.com'
        })

        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Dirección completa',
            'required': True
        })
        
        self.fields['ciudad'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ciudad',
            'required': True
        })
        
        self.fields['departamento'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Departamento/Estado',
            'required': True
        })
        
        self.fields['categoria_principal'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })

        self.fields['contacto_principal'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre del contacto principal',
            'required': True
        })

        self.fields['telefono_contacto'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Teléfono del contacto (opcional)'
        })
        
        self.fields['email_contacto'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email del contacto (opcional)'
        })

        self.fields['condiciones_pago'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Condiciones de pago (ej: 30 días, contado, etc.)',
            'rows': 3
        })

        self.fields['tiempo_entrega_dias'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Días de entrega',
            'min': '1',
            'type': 'number'
        })

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if numero_documento:
            # Verificar si ya existe otro proveedor con el mismo número de documento
            existing = Proveedor.objects.filter(numero_documento=numero_documento, activo=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un proveedor registrado con este número de documento.')
        return numero_documento

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Validación adicional de email si se proporciona
            if '@' not in email or '.' not in email:
                raise ValidationError('Por favor ingrese un email válido.')
        return email


class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = [
            'tipo_documento', 'numero_documento', 'nombres', 'apellidos',
            'telefono', 'email', 'direccion', 'especialidades',
            'nivel_experiencia', 'certificaciones', 'fecha_ingreso', 'salario',
            'estado_actual'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['tipo_documento'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['numero_documento'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Número de identificación',
            'required': True
        })

        self.fields['nombres'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombres del técnico',
            'required': True
        })

        self.fields['apellidos'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Apellidos del técnico',
            'required': True
        })

        self.fields['telefono'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Número de teléfono',
            'required': True
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'required': True
        })
        
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Dirección de residencia',
            'required': True
        })
        
        self.fields['especialidades'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Especialidades técnicas del técnico',
            'rows': 3,
            'required': True
        })
        
        self.fields['nivel_experiencia'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['certificaciones'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Certificaciones obtenidas',
            'rows': 3
        })
        
        self.fields['fecha_ingreso'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True
        })
        
        self.fields['salario'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Salario mensual',
            'step': '0.01',
            'required': True
        })
        
        self.fields['estado_actual'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if numero_documento:
            existing = Tecnico.objects.filter(numero_documento=numero_documento, activo=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un técnico registrado con este número de documento.')
        return numero_documento


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'codigo_equipo', 'nombre', 'cliente', 'tipo_equipo', 'marca',
            'modelo', 'serial', 'estado_fisico', 'especificaciones'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['codigo_equipo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: EQ-001, COMP-2024-001',
            'required': True
        })
        
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre descriptivo del equipo',
            'required': True
        })
        
        self.fields['cliente'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['tipo_equipo'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['marca'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['modelo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Modelo del equipo',
            'required': True
        })
        
        self.fields['serial'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Número de serie único',
            'required': True
        })
        
        self.fields['estado_fisico'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['especificaciones'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Especificaciones técnicas del equipo (CPU, RAM, Disco, etc.)',
            'rows': 4
        })

    def clean_codigo_equipo(self):
        codigo = self.cleaned_data.get('codigo_equipo')
        if codigo:
            existing = Equipo.objects.filter(codigo_equipo=codigo, activo=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un equipo registrado con este código.')
        return codigo

    def clean_serial(self):
        serial = self.cleaned_data.get('serial')
        if serial:
            existing = Equipo.objects.filter(serial=serial, activo=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un equipo registrado con este número de serie.')
        return serial


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'descripcion', 'pais_origen', 'sitio_web']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de la marca',
            'required': True
        })
        
        self.fields['descripcion'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Descripción de la marca',
            'rows': 3
        })
        
        self.fields['pais_origen'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'País de origen de la marca'
        })
        
        self.fields['sitio_web'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'https://www.ejemplo.com'
        })

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            existing = Marca.objects.filter(nombre__iexact=nombre, activa=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe una marca registrada con este nombre.')
        return nombre


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = [
            'numero_compra', 'proveedor', 'fecha_solicitud', 'estado',
            'subtotal', 'impuestos', 'total', 'metodo_pago', 'observaciones'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['numero_compra'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: COM-2024-001',
            'required': True
        })
        
        self.fields['proveedor'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['fecha_solicitud'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True
        })
        
        self.fields['estado'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['subtotal'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
        
        self.fields['impuestos'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
        
        self.fields['total'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
        
        self.fields['metodo_pago'].widget.attrs.update({
            'class': 'form-control'
        })
        
        self.fields['observaciones'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Observaciones sobre la compra',
            'rows': 3
        })

    def clean_numero_compra(self):
        numero = self.cleaned_data.get('numero_compra')
        if numero:
            existing = Compra.objects.filter(numero_compra=numero)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe una compra registrada con este número.')
        return numero

    def clean(self):
        cleaned_data = super().clean()
        subtotal = cleaned_data.get('subtotal', 0)
        impuestos = cleaned_data.get('impuestos', 0)
        total = cleaned_data.get('total', 0)
        
        if subtotal and impuestos and total:
            calculated_total = subtotal + impuestos
            if abs(calculated_total - total) > 0.01:  # Permitir diferencias menores por redondeo
                raise ValidationError('El total no coincide con la suma del subtotal más los impuestos.')
        
        return cleaned_data
