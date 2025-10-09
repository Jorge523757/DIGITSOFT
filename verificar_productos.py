import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DigitSoftProyecto.settings')
django.setup()

from inventario.models import Producto, Marca

print("=" * 60)
print("VERIFICACIÓN DE PRODUCTOS Y MARCAS")
print("=" * 60)

# Contar productos
total_productos = Producto.objects.count()
productos_activos = Producto.objects.filter(activo=True).count()
productos_con_stock = Producto.objects.filter(activo=True, stock_actual__gt=0).count()
marcas_activas = Marca.objects.filter(activa=True).count()

print(f"\n📦 Productos totales: {total_productos}")
print(f"✅ Productos activos: {productos_activos}")
print(f"📊 Productos con stock: {productos_con_stock}")
print(f"🏷️  Marcas activas: {marcas_activas}")

# Mostrar productos
if productos_activos > 0:
    print("\n" + "=" * 60)
    print("PRODUCTOS ACTIVOS:")
    print("=" * 60)
    for p in Producto.objects.filter(activo=True)[:10]:
        print(f"\n🔹 {p.nombre}")
        print(f"   Código: {p.codigo_producto}")
        print(f"   Marca: {p.marca.nombre if p.marca else 'Sin marca'}")
        print(f"   Categoría: {p.get_categoria_display()}")
        print(f"   Precio: ${p.precio_venta:,.0f}")
        print(f"   Stock: {p.stock_actual}")
        print(f"   Imagen: {'✓' if p.imagen else '✗'}")
else:
    print("\n⚠️  NO HAY PRODUCTOS ACTIVOS")
    print("   Necesitas crear productos desde el panel de administrador")

# Mostrar marcas
if marcas_activas > 0:
    print("\n" + "=" * 60)
    print("MARCAS ACTIVAS:")
    print("=" * 60)
    for m in Marca.objects.filter(activa=True):
        cant_productos = Producto.objects.filter(marca=m, activo=True).count()
        print(f"🏷️  {m.nombre} - {cant_productos} productos")
else:
    print("\n⚠️  NO HAY MARCAS ACTIVAS")
    print("   Necesitas crear marcas desde el panel de administrador")

print("\n" + "=" * 60)

