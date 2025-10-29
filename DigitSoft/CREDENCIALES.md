
3. **Registro Público:**
   - Los usuarios registrados públicamente son siempre **CLIENTES**
   - Solo los administradores pueden crear otros tipos de usuarios
   - Los clientes tienen acceso limitado al sistema

4. **Recuperación de Contraseña:**
   - Funciona con códigos de 6 dígitos enviados por correo
   - El código expira en 1 hora
   - Se puede solicitar un nuevo código si expira

---

## 🚀 Próximos Pasos Recomendados

1. **Inicia sesión con el usuario admin**
2. **Cambia la contraseña predeterminada**
3. **Configura el correo electrónico en settings.py**
4. **Prueba el registro público creando una cuenta de cliente**
5. **Explora el sistema y crea otros usuarios si es necesario**

---

**Fecha de creación:** 2025-01-07  
**Sistema:** DigitSoft v1.0  
**Autor:** Sistema Automático de Configuración
# 🔐 CREDENCIALES DE ACCESO - DigitSoft

## 👤 Usuario Administrador Predeterminado

He creado un usuario administrador para que puedas acceder al sistema:

### Credenciales:
- **Usuario:** `admin`
- **Contraseña:** `Admin123456`
- **Tipo:** Super Administrador
- **Correo:** admin@digitsoft.com

### Acceso al sistema:
1. Ve a: http://127.0.0.1:8000/autenticacion/login/
2. Ingresa el usuario: `admin`
3. Ingresa la contraseña: `Admin123456`
4. Haz clic en "Iniciar Sesión"

⚠️ **IMPORTANTE:** Por seguridad, cambia la contraseña después del primer inicio de sesión.

---

## ✅ Mejoras Implementadas

### 1. **Enlace de Registro en el Login**
- Ahora en la página de login aparece un enlace "Registrarse ahora"
- Los usuarios pueden crear sus propias cuentas sin necesidad de un administrador

### 2. **Sistema de Registro Público**
- URL: http://127.0.0.1:8000/autenticacion/registro/
- Los usuarios se registran automáticamente como **CLIENTE**
- Formulario completo con validación de datos
- Envío de correo de bienvenida automático

### 3. **Verificación por Correo (Ya implementada)**
- Al registrarse, el usuario recibe un correo de bienvenida
- Al recuperar contraseña, recibe un código de 6 dígitos
- Sistema de tokens con expiración de 1 hora

### 4. **Usuario Administrador Predeterminado**
- Creado automáticamente con el comando `crear_admin`
- Acceso completo al sistema
- Puede crear otros usuarios y administradores

---

## 📋 Funcionalidades del Sistema de Autenticación

### Para Usuarios NO Registrados:
1. **Iniciar Sesión** - `/autenticacion/login/`
2. **Registrarse** - `/autenticacion/registro/`
3. **Recuperar Contraseña** - `/autenticacion/recuperar-password/`

### Para Usuarios Registrados:
1. **Dashboard** - `/administrador/` (según tipo de usuario)
2. **Cerrar Sesión** - `/autenticacion/logout/`

### Para Administradores:
1. **Crear Usuarios** - `/autenticacion/admin/registro/`
2. **Gestionar Usuarios** - `/autenticacion/usuarios/`
3. **Activar/Desactivar Usuarios** - Desde la lista de usuarios

---

## 📧 Configuración de Correo Electrónico

### Estado Actual:
El sistema está configurado para enviar correos a través de Gmail.

### Para que funcione el envío de correos:
1. Abre el archivo: `DigitSoftProyecto/settings.py`
2. Busca la sección de configuración de correo (al final del archivo)
3. Reemplaza las siguientes líneas:

```python
EMAIL_HOST_USER = 'tucorreo@gmail.com'  # ← Cambia esto por tu correo
EMAIL_HOST_PASSWORD = 'tucontraseña'  # ← Cambia esto por tu contraseña de aplicación
```

### Cómo obtener una contraseña de aplicación de Gmail:
1. Ve a tu cuenta de Google
2. Seguridad → Verificación en 2 pasos (actívala si no la tienes)
3. Contraseñas de aplicaciones
4. Genera una nueva contraseña para "Correo"
5. Copia esa contraseña y pégala en `EMAIL_HOST_PASSWORD`

---

## 🎯 Cómo Usar el Sistema

### Opción 1: Registrarse como Cliente
1. Ve a http://127.0.0.1:8000/
2. Haz clic en "Iniciar Sesión"
3. Haz clic en "Registrarse ahora"
4. Completa el formulario de registro
5. Acepta los términos y condiciones
6. Haz clic en "Crear Cuenta"
7. Recibirás un mensaje de confirmación
8. Inicia sesión con tus credenciales

### Opción 2: Usar el Administrador Predeterminado
1. Ve a http://127.0.0.1:8000/autenticacion/login/
2. Usuario: `admin`
3. Contraseña: `Admin123456`
4. Haz clic en "Iniciar Sesión"

---

## 🔄 Tipos de Usuario y Sus Accesos

### 🔴 Super Administrador (admin)
- Acceso completo al sistema
- Crear, editar y eliminar usuarios
- Gestión de configuración
- Acceso al panel de Django Admin

### 🟠 Administrador
- Crear y gestionar usuarios (excepto super admins)
- Gestión de productos, ventas y compras
- Reportes y estadísticas

### 🟢 Cliente (Registro Público)
- Comprar productos en la tienda
- Ver historial de órdenes
- Seguimiento de servicios técnicos
- Gestionar perfil personal

### 🔵 Técnico
- Ver y gestionar órdenes de servicio
- Actualizar reparaciones
- Gestionar garantías

### 🟣 Proveedor
- Ver órdenes de compra
- Actualizar entregas
- Consultar inventario

---

## 🛠️ Comandos Útiles

### Crear usuario administrador adicional:
```bash
python manage.py crear_admin
```

### Crear superusuario manualmente:
```bash
python manage.py createsuperuser
```

### Ver todos los usuarios:
- Como admin, ve a: http://127.0.0.1:8000/autenticacion/usuarios/

---

## 📝 Notas Importantes

1. **Seguridad:** 
   - Las contraseñas están encriptadas en la base de datos
   - Nunca compartas tus credenciales de administrador
   - Cambia la contraseña predeterminada después del primer uso

2. **Correos:**
   - El sistema envía correos de bienvenida automáticamente
   - Los códigos de recuperación expiran en 1 hora
   - Configura el correo de Gmail para que funcione correctamente

