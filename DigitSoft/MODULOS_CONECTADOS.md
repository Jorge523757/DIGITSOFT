# CONEXIONES ENTRE MÓDULOS - DIGIT SOFT

## ✅ Resumen de Relaciones Implementadas

### 🔗 **COMPRAS**
- `proveedor` → ForeignKey a **Proveedor**
- `solicitado_por` → ForeignKey a **Administrador** 
- `aprobado_por` → ForeignKey a **Administrador**
- Incluye modelo **DetalleCompra** que relaciona:
  - `compra` → ForeignKey a **Compra**
  - `producto` → ForeignKey a **Producto**

### 🔗 **VENTAS**
- `cliente` → ForeignKey a **Cliente**
- `vendedor` → ForeignKey a **Administrador**
- Incluye modelo **DetalleVenta** que relaciona:
  - `venta` → ForeignKey a **Venta**
  - `producto` → ForeignKey a **Producto**

### 🔗 **ÓRDENES DE SERVICIO**
- `cliente` → ForeignKey a **Cliente**
- `equipo` → ForeignKey a **Equipo**
- `tecnico_asignado` → ForeignKey a **Técnico**
- `creado_por` → ForeignKey a **Administrador**
- Incluye modelo **DetalleOrdenServicio** que relaciona:
  - `orden` → ForeignKey a **OrdenServicio**
  - `servicio` → ForeignKey a **ServicioTecnico**
- Incluye modelo **RepuestoOrden** que relaciona:
  - `orden` → ForeignKey a **OrdenServicio**
  - `producto` → ForeignKey a **Producto**

### 🔗 **PRODUCTOS**
- `marca` → ForeignKey a **Marca**
- `proveedor_principal` → ForeignKey a **Proveedor**

### 🔗 **EQUIPOS**
- `marca` → ForeignKey a **Marca**
- `cliente` → ForeignKey a **Cliente** (propietario)

### 🔗 **CARRITOS**
- `cliente` → ForeignKey a **Cliente**
- `venta_generada` → OneToOneField a **Venta**
- Incluye modelo **DetalleCarrito** que relaciona:
  - `carrito` → ForeignKey a **Carrito**
  - `producto` → ForeignKey a **Producto**

### 🔗 **GARANTÍAS**
- `producto` → ForeignKey a **Producto**
- `equipo` → ForeignKey a **Equipo**
- `cliente` → ForeignKey a **Cliente**
- `venta` → ForeignKey a **Venta**

### 🔗 **FACTURAS**
- `cliente` → ForeignKey a **Cliente**
- `venta` → OneToOneField a **Venta**
- `orden_servicio` → OneToOneField a **OrdenServicio**
- `emitida_por` → ForeignKey a **Administrador**

### 🔗 **LOG DE ACTIVIDADES**
- `administrador` → ForeignKey a **Administrador**

---

## 📊 Propiedades Calculadas Agregadas

### **Cliente**
- `total_compras` - Total de compras pagadas
- `tiene_ordenes_pendientes` - Verifica órdenes pendientes

### **Técnico**
- `ordenes_activas` - Cuenta órdenes en proceso
- `puede_recibir_orden` - Verifica disponibilidad

### **Marca**
- `total_productos` - Cuenta productos activos
- `total_equipos` - Cuenta equipos registrados

### **Proveedor**
- `total_compras_realizadas` - Compras pagadas
- `monto_total_comprado` - Suma total comprado
- `productos_suministrados` - Productos que suministra

### **Producto**
- `veces_vendido` - Total de unidades vendidas

### **Equipo**
- `historial_servicios` - Lista de servicios realizados
- `esta_en_servicio` - Verifica si está en reparación

### **ServicioTecnico**
- `veces_solicitado` - Veces que se ha solicitado

### **OrdenServicio**
- `dias_en_servicio` - Días que lleva en servicio
- `esta_atrasada` - Verifica si está atrasada

### **Compra**
- `total_productos` - Total de productos en la compra

### **Venta**
- `total_productos` - Total de productos vendidos
- `utilidad` - Calcula la ganancia de la venta

### **Garantia**
- `esta_vigente` - Verifica si está vigente

---

## 🆕 Modelos Nuevos Creados

1. **DetalleCompra** - Detalle de productos en compras
2. **DetalleVenta** - Detalle de productos en ventas
3. **DetalleOrdenServicio** - Servicios aplicados en órdenes
4. **RepuestoOrden** - Repuestos usados en órdenes de servicio
5. **DetalleCarrito** - Items dentro de un carrito
6. **ConfiguracionGeneral** - Configuraciones del sistema

---

## 🎯 Flujo de Trabajo Integrado

### **Proceso de Compra:**
1. **Administrador** solicita compra
2. Selecciona **Proveedor**
3. Agrega **Productos** en **DetalleCompra**
4. **Administrador** con permisos aprueba
5. Al recibir, actualiza stock de **Productos**

### **Proceso de Venta:**
1. **Cliente** agrega productos a **Carrito**
2. **DetalleCarrito** registra cada producto
3. Al finalizar, **Carrito** se convierte en **Venta**
4. **DetalleVenta** copia items del carrito
5. **Administrador**/Vendedor procesa la venta
6. Se genera **Factura** y **Garantía**

### **Proceso de Servicio Técnico:**
1. **Cliente** trae **Equipo**
2. **Administrador** crea **OrdenServicio**
3. Asigna **Técnico**
4. **DetalleOrdenServicio** registra servicios aplicados
5. **RepuestoOrden** registra repuestos usados
6. Al completar se genera **Factura**
7. Se actualiza estado del **Equipo**

---

## 📝 Ejemplo de Uso en el Código

```python
# Obtener todas las compras de un proveedor
proveedor = Proveedor.objects.get(id=1)
compras = proveedor.compras.all()

# Obtener todas las ventas de un cliente
cliente = Cliente.objects.get(id=1)
ventas = cliente.ventas.all()

# Obtener órdenes asignadas a un técnico
tecnico = Tecnico.objects.get(id=1)
ordenes = tecnico.ordenes_asignadas.filter(estado='PENDIENTE')

# Obtener productos de una marca
marca = Marca.objects.get(id=1)
productos = marca.productos.all()

# Obtener equipos de un cliente
cliente = Cliente.objects.get(id=1)
equipos = cliente.equipos.all()

# Obtener el carrito activo de un cliente
carrito = Carrito.objects.filter(cliente=cliente, estado='ACTIVO').first()

# Obtener detalles de una compra
compra = Compra.objects.get(id=1)
detalles = compra.detalles.all()
for detalle in detalles:
    print(f"{detalle.producto.nombre}: {detalle.cantidad}")

# Obtener servicios aplicados en una orden
orden = OrdenServicio.objects.get(id=1)
servicios = orden.servicios_aplicados.all()
repuestos = orden.repuestos_utilizados.all()
```

---

## ✅ Estado del Sistema

✔️ Todos los módulos están conectados
✔️ Relaciones ForeignKey implementadas
✔️ Modelos de detalle creados
✔️ Propiedades calculadas agregadas
✔️ Métodos de validación implementados
✔️ Sistema completamente integrado

El sistema ahora funciona como un **ERP completo** donde todos los módulos se comunican entre sí.

