# 🔐 Sistema de Tipos de Usuario - DigitSoft

## ¿Cómo se identifica el tipo de usuario?

El sistema **identifica automáticamente** el tipo de usuario al iniciar sesión mediante el modelo `PerfilUsuario` que está vinculado a cada cuenta.

## 📋 Tipos de Usuario Disponibles

### 1. 🔴 SUPER_ADMIN (Super Administrador)
- **Acceso:** Completo al sistema
- **Permisos:**
  - Crear, editar y eliminar usuarios
  - Acceso a todas las funcionalidades del sistema
  - Gestión de configuración general
  - Acceso al panel de administración de Django
- **Características especiales:**
  - `is_staff = True`
  - `is_superuser = True`
  - `puede_crear_usuarios = True`

### 2. 🟠 ADMINISTRADOR (Administrador)
- **Acceso:** Gestión completa del negocio
- **Permisos:**
  - Crear y gestionar usuarios (excepto super admins)
  - Gestión de productos, ventas y compras
  - Reportes y estadísticas
  - Gestión de órdenes de servicio
- **Características especiales:**
  - `is_staff = True`
  - `puede_crear_usuarios = True`

### 3. 🟢 CLIENTE (Cliente)
- **Acceso:** Área de compras y seguimiento
- **Permisos:**
  - Ver catálogo de productos
  - Realizar compras en la tienda
  - Ver historial de órdenes
  - Seguimiento de servicios técnicos solicitados
  - Gestionar su perfil

### 4. 🔵 TECNICO (Técnico)
- **Acceso:** Área de servicios técnicos
- **Permisos:**
  - Ver y gestionar órdenes de servicio asignadas
  - Actualizar estado de reparaciones
  - Registrar diagnósticos y trabajos realizados
  - Ver inventario de repuestos
  - Gestionar garantías

### 5. 🟣 PROVEEDOR (Proveedor)
- **Acceso:** Área de inventario y productos
- **Permisos:**
  - Ver órdenes de compra
  - Actualizar estado de entregas
  - Consultar productos y stock
  - Ver historial de transacciones

## 🔄 Proceso de Identificación

### 1. Al Crear el Usuario
```python
# El administrador crea el usuario y asigna el tipo
PerfilUsuario.objects.create(
    user=user,
    tipo_usuario='CLIENTE',  # o ADMINISTRADOR, TECNICO, etc.
    documento='123456789',
    telefono='3001234567'
)
```

### 2. Al Iniciar Sesión
```python
# El sistema verifica automáticamente:
1. Usuario y contraseña correctos
2. Existe un perfil asociado (PerfilUsuario)
3. El perfil está activo (estado = 'ACTIVO')
4. Obtiene el tipo_usuario del perfil
5. Muestra mensaje: "Has iniciado sesión como [Tipo de Usuario]"
```

### 3. En el Dashboard
```python
# El dashboard se adapta según el tipo de usuario
if request.user.perfil.tipo_usuario == 'CLIENTE':
    # Mostrar opciones de compra y seguimiento
elif request.user.perfil.tipo_usuario == 'TECNICO':
    # Mostrar órdenes de servicio
elif request.user.perfil.tipo_usuario in ['ADMINISTRADOR', 'SUPER_ADMIN']:
    # Mostrar panel completo de administración
```

## 📊 Verificación en el Código

### En las Vistas
```python
# Verificar tipo de usuario
@login_required
def mi_vista(request):
    if request.user.perfil.tipo_usuario == 'ADMINISTRADOR':
        # Código para administradores
        pass
    elif request.user.perfil.tipo_usuario == 'CLIENTE':
        # Código para clientes
        pass
```

### En los Templates
```html
{% if user.perfil.tipo_usuario == 'ADMINISTRADOR' %}
    <button>Panel de Administración</button>
{% endif %}

{% if user.perfil.tipo_usuario == 'CLIENTE' %}
    <button>Mis Compras</button>
{% endif %}
```

## 🎯 Mejoras Implementadas

1. **Mensaje de Bienvenida Mejorado:**
   - Ahora muestra: "¡Bienvenido [Nombre]! Has iniciado sesión como [Tipo de Usuario]"

2. **Información Visual en Login:**
   - Panel informativo que explica los diferentes tipos de usuario
   - Lista de permisos por tipo

3. **Identificación Automática:**
   - No necesitas seleccionar tu tipo al iniciar sesión
   - El sistema lo detecta automáticamente desde tu perfil

## 🔧 Cómo Crear Usuarios con Diferentes Tipos

### Opción 1: Desde el Panel de Administración
1. Inicia sesión como Administrador
2. Ve a "Gestión de Usuarios" (http://localhost:8000/autenticacion/usuarios/)
3. Haz clic en "Crear Nuevo Usuario"
4. Completa el formulario y selecciona el "Tipo de Usuario"
5. El sistema asignará automáticamente los permisos correspondientes

### Opción 2: Usando el Admin de Django
1. Ve a http://localhost:8000/admin/
2. Inicia sesión con una cuenta de Super Admin
3. Crea un User y su PerfilUsuario asociado
4. Selecciona el tipo_usuario deseado

### Opción 3: Por Código (Para desarrollo)
```python
from django.contrib.auth.models import User
from autenticacion.models import PerfilUsuario

# Crear usuario cliente
user = User.objects.create_user(
    username='cliente1',
    email='cliente@ejemplo.com',
    password='password123',
    first_name='Juan',
    last_name='Pérez'
)

perfil = PerfilUsuario.objects.create(
    user=user,
    tipo_usuario='CLIENTE',
    documento='123456789',
    telefono='3001234567'
)
```

## 📌 Importante

- **Un usuario solo puede tener UN tipo** a la vez
- **El tipo se define al crear la cuenta** y puede ser modificado por un administrador
- **El sistema valida automáticamente** que el usuario tenga un perfil activo antes de permitir el acceso
- **Cada tipo tiene permisos específicos** que se aplican en todo el sistema

## 🔍 Para Verificar tu Tipo de Usuario

1. Inicia sesión en el sistema
2. Observa el mensaje de bienvenida: mostrará tu tipo de usuario
3. O ve al dashboard y verás las opciones disponibles según tu tipo

---

**Fecha de creación:** 2025-01-07
**Sistema:** DigitSoft v1.0

