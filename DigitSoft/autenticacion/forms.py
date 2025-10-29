from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión personalizado"""

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario o Correo Electrónico',
            'autocomplete': 'username',
            'id': 'id_username'
        }),
        label='Usuario'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
            'id': 'id_password'
        }),
        label='Contraseña'
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        }),
        label='Recordarme'
    )


class RegistroUsuarioForm(UserCreationForm):
    """Formulario para registro de nuevos usuarios"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'id': 'id_email'
        }),
        label='Correo Electrónico'
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres',
            'id': 'id_first_name'
        }),
        label='Nombres'
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos',
            'id': 'id_last_name'
        }),
        label='Apellidos'
    )

    telefono = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
            'id': 'id_telefono'
        }),
        label='Teléfono'
    )

    documento = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de documento',
            'id': 'id_documento'
        }),
        label='Documento'
    )

    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_USUARIO_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_usuario'
        }),
        label='Tipo de Usuario'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'id_password1'
        }),
        label='Contraseña'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
            'id': 'id_password2'
        }),
        label='Confirmar Contraseña'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'id': 'id_username'
            })
        }
        labels = {
            'username': 'Nombre de Usuario'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if PerfilUsuario.objects.filter(documento=documento).exists():
            raise forms.ValidationError('Este documento ya está registrado.')
        return documento


class RecuperacionPasswordForm(forms.Form):
    """Formulario para solicitar recuperación de contraseña"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'id': 'id_email',
            'autocomplete': 'email'
        }),
        label='Correo Electrónico',
        help_text='Ingresa tu correo electrónico registrado'
    )


class VerificarCodigoForm(forms.Form):
    """Formulario para verificar el código enviado por correo"""

    codigo = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '000000',
            'id': 'id_codigo',
            'style': 'font-size: 24px; letter-spacing: 10px;',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        }),
        label='Código de Verificación',
        help_text='Ingresa el código de 6 dígitos enviado a tu correo'
    )


class NuevaPasswordForm(forms.Form):
    """Formulario para establecer nueva contraseña"""

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva Contraseña',
            'id': 'id_new_password1',
            'autocomplete': 'new-password'
        }),
        label='Nueva Contraseña',
        min_length=8,
        help_text='Mínimo 8 caracteres'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
            'id': 'id_new_password2',
            'autocomplete': 'new-password'
        }),
        label='Confirmar Contraseña'
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data


class RegistroPublicoForm(UserCreationForm):
    """Formulario para registro público de clientes"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'id': 'id_email'
        }),
        label='Correo Electrónico'
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres',
            'id': 'id_first_name'
        }),
        label='Nombres'
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos',
            'id': 'id_last_name'
        }),
        label='Apellidos'
    )

    telefono = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
            'id': 'id_telefono'
        }),
        label='Teléfono'
    )

    documento = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de documento',
            'id': 'id_documento'
        }),
        label='Documento de Identidad'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'id_password1'
        }),
        label='Contraseña',
        min_length=8,
        help_text='Mínimo 8 caracteres'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
            'id': 'id_password2'
        }),
        label='Confirmar Contraseña'
    )

    acepto_terminos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'acepto_terminos'
        }),
        label='Acepto los términos y condiciones'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'id': 'id_username'
            })
        }
        labels = {
            'username': 'Nombre de Usuario'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if PerfilUsuario.objects.filter(documento=documento).exists():
            raise forms.ValidationError('Este documento ya está registrado.')
        return documento
