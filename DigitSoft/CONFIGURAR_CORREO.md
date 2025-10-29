# 📧 Configuración de Correo Electrónico para Recuperación de Contraseña

## ❗ Problema Actual

El sistema de recuperación de contraseña **NO está enviando códigos** porque falta configurar las credenciales reales del correo electrónico.

**Error mostrado:** `ascii codec can't encode character '\xff1' in position 30: ordinal not in range(128)`

**Causa:** Las credenciales de correo en `settings.py` son de ejemplo y no son válidas.

---

## ✅ Solución: Configurar Gmail

### **Paso 1: Generar una Contraseña de Aplicación en Gmail**

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú lateral, haz clic en **"Seguridad"**
3. Busca la sección **"Verificación en dos pasos"**
   - Si NO está activada, **ACTÍVALA PRIMERO** (es obligatorio)
4. Una vez activada, regresa a "Seguridad"
5. Busca **"Contraseñas de aplicaciones"** (aparece solo si tienes 2FA activado)
6. Selecciona:
   - App: **"Correo"**
   - Dispositivo: **"Otro (nombre personalizado)"** → escribe "DigitSoft"
7. Haz clic en **"Generar"**
8. **COPIA** la contraseña de 16 caracteres que aparece (sin espacios)

### **Paso 2: Actualizar settings.py**

Abre el archivo: `DigitSoftProyecto/settings.py`

Busca la sección de EMAIL (línea 147-153) y actualiza:

```python
# Configuración del correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jorgedavidcristanchoguarin@gmail.com'  # ✅ Ya configurado
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # ⚠️ PEGA AQUÍ tu contraseña de aplicación
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

**IMPORTANTE:** 
- Usa la **contraseña de aplicación** generada (16 caracteres)
- **NO** uses tu contraseña normal de Gmail
- Pega la contraseña **sin espacios**

### **Paso 3: Reiniciar el servidor**

Después de actualizar `settings.py`:

1. Detén el servidor Django (Ctrl + C)
2. Vuelve a ejecutar:
   ```bash
   python manage.py runserver
   ```

### **Paso 4: Probar la recuperación**

1. Ve a: http://127.0.0.1:8000/autenticacion/recuperar-password/
2. Ingresa: `jorgedavidcristanchoguarin@gmail.com`
3. Haz clic en **"Enviar Código de Verificación"**
4. Revisa tu bandeja de entrada (puede tardar unos segundos)

---

## 🔄 Alternativa: Modo de Desarrollo (Sin Correo Real)

Si solo quieres **probar** sin configurar Gmail, puedes usar el backend de consola:

### En settings.py, cambia:

```python
# Modo desarrollo - Los correos se muestran en la consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Con esto, los códigos de verificación **se mostrarán en la terminal** donde corre el servidor, en lugar de enviarse por correo.

---

## 📋 Resumen de Estados

| Configuración | Estado Actual | Acción Requerida |
|---------------|---------------|------------------|
| EMAIL_HOST_USER | ✅ Configurado | Ninguna |
| EMAIL_HOST_PASSWORD | ❌ Falta | Generar contraseña de app |
| Servidor SMTP | ✅ Gmail configurado | Ninguna |

---

## 🆘 Solución de Problemas

### Error: "SMTPAuthenticationError"
- **Causa:** Contraseña incorrecta
- **Solución:** Verifica que usaste la contraseña de aplicación, no tu contraseña normal

### Error: "SMTPServerDisconnected"
- **Causa:** Firewall o conexión bloqueada
- **Solución:** Verifica tu conexión a Internet

### No llega el correo
- **Revisa:** Carpeta de SPAM
- **Verifica:** Que el correo del usuario existe en la base de datos
- **Tiempo:** Puede tardar hasta 1-2 minutos

---

## ✨ Próximos Pasos

1. ✅ Genera la contraseña de aplicación en Gmail
2. ✅ Actualiza `EMAIL_HOST_PASSWORD` en settings.py
3. ✅ Reinicia el servidor
4. ✅ Prueba la recuperación de contraseña

**¡Listo! El sistema estará funcionando correctamente.**

