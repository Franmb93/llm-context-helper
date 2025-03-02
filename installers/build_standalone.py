#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar un ejecutable independiente del Selector de Contexto.
Utiliza PyInstaller para crear un archivo binario standalone.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import platform

def main():
    """Función principal para generar el ejecutable."""
    print("Generando ejecutable independiente para el Selector de Contexto...")
    
    # Obtener la ruta absoluta al directorio del proyecto
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Definir rutas absolutas para los recursos
    assets_dir = os.path.join(project_dir, "assets")
    config_dir = os.path.join(project_dir, "config")
    resources_dir = os.path.join(project_dir, "resources")
    src_dir = os.path.join(project_dir, "src")
    
    # Verificar que las carpetas existen
    print("Verificando directorios de recursos:")
    missing_dirs = []
    
    for dir_path, dir_name in [
        (assets_dir, "assets"),
        (config_dir, "config"),
        (resources_dir, "resources"),
        (src_dir, "src")
    ]:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)
            print(f"  ✗ No se encuentra: {dir_path}")
        else:
            print(f"  ✓ Encontrado: {dir_path}")
    
    if missing_dirs:
        print(f"\nERROR: No se encuentran los siguientes directorios: {', '.join(missing_dirs)}")
        print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto.")
        return 1
    
    # Crear un archivo temporal con el código bootstrap para PyInstaller
    temp_dir = tempfile.mkdtemp()
    bootstrap_path = os.path.join(temp_dir, "context_selector_bootstrap.py")
    
    with open(bootstrap_path, 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Script de arranque para el Selector de Contexto con soporte para ejecución en modo frozen.
\"\"\"

import os
import sys

# Ajustar el path para importaciones ya sea en modo desarrollo o congelado
if getattr(sys, 'frozen', False):
    # Se está ejecutando desde un bundle congelado
    bundle_dir = os.path.dirname(sys.executable)
    # Añadir todas las rutas necesarias para el modo congelado
    sys.path.insert(0, bundle_dir)
else:
    # Se está ejecutando en modo de desarrollo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(script_dir, '..')))

# Importar la aplicación principal
from src.core.app import ContextSelectorApp

def main():
    \"\"\"Iniciar la aplicación.\"\"\"
    app = ContextSelectorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
""")
    
    print(f"Archivo de arranque creado en: {bootstrap_path}")
    
    # Variable para la ruta de PyInstaller
    pyinstaller_exe = "pyinstaller"  # Por defecto, buscar en PATH
    
    # Construir los argumentos para PyInstaller
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--name=SelectorDeContexto",
        "--onefile",
        "--windowed",  # Sin consola
        "--clean",
        "--distpath=" + os.path.join(project_dir, "dist"),
        "--workpath=" + os.path.join(project_dir, "build"),
        "--specpath=" + os.path.join(project_dir, "build"),
    ]
    
    # Añadir icono si existe
    icon_path = os.path.join(project_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        pyinstaller_args.append(f"--icon={icon_path}")
    
    # Añadir el bootstrapper como archivo principal
    pyinstaller_args.append(bootstrap_path)
    
    # Añadir datos adicionales (assets, config, resources)
    os_path_sep = ";" if sys.platform == "win32" else ":"
    pyinstaller_args.extend([
        "--add-data", f"{assets_dir}{os_path_sep}assets",
        "--add-data", f"{config_dir}{os_path_sep}config",
        "--add-data", f"{resources_dir}{os_path_sep}resources"
    ])
    
    # Añadir src como directorio importable
    pyinstaller_args.extend([
        "--add-data", f"{src_dir}{os_path_sep}src"  
    ])
    
    # Ejecutar PyInstaller
    print("Ejecutando PyInstaller con los siguientes argumentos:")
    print(" ".join(pyinstaller_args))
    
    try:
        process = subprocess.Popen(
            pyinstaller_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Mostrar salida en tiempo real
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Esperar a que termine
        process.wait()
        
        if process.returncode == 0:
            # Nombre del ejecutable según el sistema operativo
            exe_name = "SelectorDeContexto.exe" if sys.platform == "win32" else "SelectorDeContexto"
            exe_path = os.path.join(project_dir, "dist", exe_name)
            
            print("\n¡Ejecutable generado correctamente!")
            print(f"Ejecutable ubicado en: {os.path.abspath(exe_path)}")
            
            return 0
        else:
            print(f"Error al generar el ejecutable (código {process.returncode})")
            return 1
        
    except Exception as e:
        print(f"Error al generar el ejecutable: {e}")
        return 1
    finally:
        # Limpiar archivos temporales
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
