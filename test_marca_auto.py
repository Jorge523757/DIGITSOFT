"""
Script de prueba automático para registrar una marca en DigitSoft
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DigitSoftProyecto.settings')
django.setup()

from administrador.models import Marca
from administrador.forms import MarcaForm

def test_crear_marca():
    """Prueba automática de creación de marca"""

    print("=" * 60)
    print("PRUEBA AUTOMÁTICA - REGISTRO DE MARCA")
    print("=" * 60)

    # Datos de prueba
    datos_marca = {
        'nombre': 'Dell Technologies',
        'tipo_marca': 'EQUIPOS',
        'descripcion': 'Marca líder en equipos de cómputo, servidores y soluciones empresariales',
        'pais_origen': 'Estados Unidos',
        'sitio_web': 'https://www.dell.com',
    }

    print("\n📝 Datos de la marca:")
    for campo, valor in datos_marca.items():
        print(f"   • {campo}: {valor}")

    # Verificar si ya existe
    marca_existente = Marca.objects.filter(nombre=datos_marca['nombre']).first()
    if marca_existente:
        print(f"\n⚠️  La marca '{datos_marca['nombre']}' ya existe.")
        print(f"   ID: {marca_existente.id}")
        print(f"   Eliminando marca anterior...")
        marca_existente.delete()
        print("   ✅ Marca anterior eliminada.")

    # Crear la marca usando el formulario
    print("\n🔄 Validando datos con el formulario...")
    form = MarcaForm(data=datos_marca)

    if form.is_valid():
        print("   ✅ Datos validados correctamente")
        marca = form.save()

        print("\n✅ ¡MARCA CREADA EXITOSAMENTE!")
        print("-" * 60)
        print(f"   ID: {marca.id}")
        print(f"   Nombre: {marca.nombre}")
        print(f"   Tipo: {marca.get_tipo_marca_display()}")
        print(f"   País: {marca.pais_origen}")
        print(f"   Sitio web: {marca.sitio_web}")
        print(f"   Activa: {'Sí' if marca.activa else 'No'}")
        print(f"   Fecha registro: {marca.fecha_registro.strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 60)

        # Verificar que se guardó en la base de datos
        print("\n🔍 Verificando en la base de datos...")
        marca_verificada = Marca.objects.get(id=marca.id)
        print(f"   ✅ Marca encontrada: {marca_verificada.nombre}")

        return True
    else:
        print("\n❌ ERROR AL VALIDAR EL FORMULARIO:")
        for campo, errores in form.errors.items():
            print(f"   • {campo}: {', '.join(errores)}")
        return False

def listar_todas_marcas():
    """Lista todas las marcas en el sistema"""

    print("\n" + "=" * 60)
    print("TODAS LAS MARCAS REGISTRADAS")
    print("=" * 60)

    marcas = Marca.objects.all().order_by('nombre')

    if marcas.exists():
        print(f"\nTotal de marcas: {marcas.count()}\n")
        for i, marca in enumerate(marcas, 1):
            print(f"{i}. {marca.nombre}")
            print(f"   Tipo: {marca.get_tipo_marca_display()}")
            print(f"   País: {marca.pais_origen or 'N/A'}")
            print(f"   Estado: {'Activa' if marca.activa else 'Inactiva'}")
            print()
    else:
        print("\n⚠️  No hay marcas registradas en el sistema.\n")

    print("=" * 60)

if __name__ == '__main__':
    try:
        # Ejecutar la prueba
        exito = test_crear_marca()

        # Listar todas las marcas
        listar_todas_marcas()

        if exito:
            print("\n✅ PRUEBA COMPLETADA EXITOSAMENTE")
        else:
            print("\n❌ LA PRUEBA FALLÓ")

    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()

