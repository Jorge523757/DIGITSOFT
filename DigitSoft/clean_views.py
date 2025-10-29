import os

# Leer el archivo
with open(r'C:\Users\jorge\OneDrive\Escritorio\DigitSoft\DIGITSOFT\administrador\views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar el inicio del docstring correcto
docstring_start = content.find('"""' + '\nDigitSoft - Módulo de Administrador')

if docstring_start > 0:
    # Eliminar todo lo que está antes del docstring correcto
    clean_content = content[docstring_start:]

    # Guardar el archivo limpio
    with open(r'C:\Users\jorge\OneDrive\Escritorio\DigitSoft\DIGITSOFT\administrador\views.py', 'w', encoding='utf-8') as f:
        f.write(clean_content)

    print(f"✅ Archivo limpiado. Se eliminaron {docstring_start} caracteres duplicados.")
else:
    print("❌ No se encontró el docstring correcto.")

