"""
Script de prueba para registrar marcas en el sistema DigitSoft
Ejecutar desde el directorio del proyecto con: python test_marca.py
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DigitSoftProyecto.settings')
django.setup()

from administrador.models import Marca
from administrador.forms import MarcaForm

def crear_marca_prueba():
    """Crea una marca de prueba en la base de datos"""

    print("=" * 60)
    print("SCRIPT DE PRUEBA - REGISTRO DE MARCA")
    print("=" * 60)

    # Datos de prueba para la marca
    datos_marca = {
        'nombre': 'Dell',
        'tipo_marca': 'EQUIPOS',
        'descripcion': 'Marca líder en equipos de cómputo y servidores empresariales',
        'pais_origen': 'Estados Unidos',
        'sitio_web': 'https://www.dell.com',
    }

    print("\n📝 Datos de la marca a registrar:")
    for campo, valor in datos_marca.items():
        print(f"   {campo}: {valor}")

    # Verificar si la marca ya existe
    if Marca.objects.filter(nombre=datos_marca['nombre']).exists():
        print(f"\n⚠️  La marca '{datos_marca['nombre']}' ya existe en la base de datos.")
        marca_existente = Marca.objects.get(nombre=datos_marca['nombre'])
        print(f"   ID: {marca_existente.id}")
        print(f"   Tipo: {marca_existente.get_tipo_marca_display()}")
        print(f"   Activa: {'Sí' if marca_existente.activa else 'No'}")

        respuesta = input("\n¿Deseas eliminarla y crear una nueva? (s/n): ")
        if respuesta.lower() == 's':
            marca_existente.delete()
            print("✅ Marca anterior eliminada.")
        else:
            print("❌ Operación cancelada.")
            return

    # Crear la marca usando el formulario
    print("\n🔄 Creando marca usando el formulario...")
    form = MarcaForm(data=datos_marca)

    if form.is_valid():
        marca = form.save()
        print("\n✅ ¡Marca creada exitosamente!")
        print(f"   ID: {marca.id}")
        print(f"   Nombre: {marca.nombre}")
        print(f"   Tipo: {marca.get_tipo_marca_display()}")
        print(f"   País: {marca.pais_origen}")
        print(f"   Sitio web: {marca.sitio_web}")
        print(f"   Fecha de registro: {marca.fecha_registro}")
        print(f"   Estado: {'Activa' if marca.activa else 'Inactiva'}")
    else:
        print("\n❌ Error al validar el formulario:")
        for campo, errores in form.errors.items():
            print(f"   {campo}: {', '.join(errores)}")

    print("\n" + "=" * 60)

def listar_marcas():
    """Lista todas las marcas registradas"""

    print("\n📋 MARCAS REGISTRADAS EN EL SISTEMA:")
    print("-" * 60)

    marcas = Marca.objects.all()

    if marcas.exists():
        for i, marca in enumerate(marcas, 1):
            print(f"\n{i}. {marca.nombre}")
            print(f"   ID: {marca.id}")
            print(f"   Tipo: {marca.get_tipo_marca_display()}")
            print(f"   País: {marca.pais_origen or 'No especificado'}")
            print(f"   Estado: {'Activa' if marca.activa else 'Inactiva'}")
            print(f"   Fecha registro: {marca.fecha_registro.strftime('%d/%m/%Y %H:%M')}")
    else:
        print("   No hay marcas registradas en el sistema.")

    print("\n" + "=" * 60)

def menu_principal():
    """Menú principal del script de prueba"""

    while True:
        print("\n" + "=" * 60)
        print("MENÚ DE PRUEBAS - GESTIÓN DE MARCAS")
        print("=" * 60)
        print("\n1. Crear marca de prueba (Dell)")
        print("2. Listar todas las marcas")
        print("3. Crear marca personalizada")
        print("4. Eliminar una marca")
        print("5. Salir")

        opcion = input("\nSelecciona una opción (1-5): ")

        if opcion == '1':
            crear_marca_prueba()
        elif opcion == '2':
            listar_marcas()
        elif opcion == '3':
            crear_marca_personalizada()
        elif opcion == '4':
            eliminar_marca()
        elif opcion == '5':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")

def crear_marca_personalizada():
    """Permite crear una marca con datos personalizados"""

    print("\n" + "=" * 60)
    print("CREAR MARCA PERSONALIZADA")
    print("=" * 60)

    print("\nTipos de marca disponibles:")
    print("1. EQUIPOS - Equipos de Cómputo")
    print("2. COMPONENTES - Componentes")
    print("3. SOFTWARE - Software")
    print("4. ACCESORIOS - Accesorios")
    print("5. CONSUMIBLES - Consumibles")

    tipo_opciones = {
        '1': 'EQUIPOS',
        '2': 'COMPONENTES',
        '3': 'SOFTWARE',
        '4': 'ACCESORIOS',
        '5': 'CONSUMIBLES'
    }

    nombre = input("\nNombre de la marca: ")
    tipo_input = input("Tipo de marca (1-5): ")
    tipo_marca = tipo_opciones.get(tipo_input, 'EQUIPOS')
    descripcion = input("Descripción: ")
    pais_origen = input("País de origen: ")
    sitio_web = input("Sitio web (opcional, ej: https://www.ejemplo.com): ")

    datos_marca = {
        'nombre': nombre,
        'tipo_marca': tipo_marca,
        'descripcion': descripcion,
        'pais_origen': pais_origen,
    }

    if sitio_web:
        datos_marca['sitio_web'] = sitio_web

    form = MarcaForm(data=datos_marca)

    if form.is_valid():
        marca = form.save()
        print(f"\n✅ ¡Marca '{marca.nombre}' creada exitosamente!")
    else:
        print("\n❌ Error al validar el formulario:")
        for campo, errores in form.errors.items():
            print(f"   {campo}: {', '.join(errores)}")

def eliminar_marca():
    """Elimina una marca del sistema"""

    print("\n" + "=" * 60)
    print("ELIMINAR MARCA")
    print("=" * 60)

    marcas = Marca.objects.all()

    if not marcas.exists():
        print("\n⚠️  No hay marcas registradas en el sistema.")
        return

    print("\nMarcas disponibles:")
    for i, marca in enumerate(marcas, 1):
        print(f"{i}. {marca.nombre} ({marca.get_tipo_marca_display()})")

    try:
        opcion = int(input("\nNúmero de la marca a eliminar (0 para cancelar): "))

        if opcion == 0:
            print("❌ Operación cancelada.")
            return

        if 1 <= opcion <= marcas.count():
            marca = list(marcas)[opcion - 1]
            nombre_marca = marca.nombre
            marca.delete()
            print(f"\n✅ Marca '{nombre_marca}' eliminada exitosamente.")
        else:
            print("\n❌ Opción no válida.")
    except ValueError:
        print("\n❌ Por favor ingresa un número válido.")

if __name__ == '__main__':
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
