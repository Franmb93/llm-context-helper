#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar un ejecutable independiente del Selector de Contexto con correcciones
para evitar problemas de importación en modo frozen.
"""

import os
import sys
import tempfile
import shutil
import subprocess

def main():
    """Función principal para generar el ejecutable."""
    print("Generando ejecutable independiente para el Selector de Contexto...")
    
    # Obtener la ruta absoluta al directorio del proyecto
    project_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Definir rutas absolutas para los recursos
    assets_dir = os.path.join(project_dir, "assets")
    config_dir = os.path.join(project_dir, "config")
    resources_dir = os.path.join(project_dir, "resources")
    src_dir = os.path.join(project_dir, "src")
    
    # Verificar que las carpetas existen
    print("Verificando directorios de recursos:")
    missing_dirs = []
    
    if not os.path.exists(assets_dir):
        missing_dirs.append("assets")
        print(f"  \u2718 No se encuentra: {assets_dir}")
    else:
        print(f"  ✔ Encontrado: {assets_dir}")
        
    if not os.path.exists(config_dir):
        missing_dirs.append("config")
        print(f"  \u2718 No se encuentra: {config_dir}")
    else:
        print(f"  ✔ Encontrado: {config_dir}")
        
    if not os.path.exists(resources_dir):
        missing_dirs.append("resources")
        print(f"  \u2718 No se encuentra: {resources_dir}")
    else:
        print(f"  ✔ Encontrado: {resources_dir}")
        
    if not os.path.exists(src_dir):
        missing_dirs.append("src")
        print(f"  \u2718 No se encuentra: {src_dir}")
    else:
        print(f"  ✔ Encontrado: {src_dir}")
    
    if missing_dirs:
        print(f"\nERROR: No se encuentran los siguientes directorios: {', '.join(missing_dirs)}")
        print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto.")
        return 1
    
    # Crear un archivo temporal con las correcciones para la ejecución dentro de un bundle
    temp_dir = tempfile.mkdtemp()
    
    # Crear un archivo temporal con un código auxiliar para la ejecución 
    # que evite problemas de importación
    bootstrapper_path = os.path.join(temp_dir, "context_selector_startup.py")
    
    with open(bootstrapper_path, 'w') as f:
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
    
    print("Archivo de arranque creado para evitar problemas de importación.")
    
    # Comando de PyInstaller para crear el ejecutable
    pyinstaller_command = [
        "python", "-m", "PyInstaller",
        "--name=SelectorDeContexto",
        "--onefile",
        "--windowed",
        "--clean",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=build"
    ]
    
    # Añadir icono si existe
    icon_path = os.path.join(project_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        pyinstaller_command.append(f"--icon={icon_path}")
    
    # Añadir el bootstrapper como archivo principal
    pyinstaller_command.append(bootstrapper_path)
    
    # Añadir datos adicionales (assets, config, resources)
    os_path_sep = ";" if sys.platform == "win32" else ":"
    pyinstaller_command.extend([
        "--add-data", f"{assets_dir}{os_path_sep}assets",
        "--add-data", f"{config_dir}{os_path_sep}config",
        "--add-data", f"{resources_dir}{os_path_sep}resources"
    ])
    
    # Añadir src como directorio importable
    pyinstaller_command.extend([
        "--add-data", f"{src_dir}{os_path_sep}src"  
    ])
    
    # Ejecutar PyInstaller
    print("Ejecutando PyInstaller con los siguientes argumentos:")
    print(" ".join(pyinstaller_command))
    
    try:
        subprocess.run(pyinstaller_command, check=True)
        
        print("\n¡Ejecutable generado correctamente!")
        
        # Mostrar ubicación del ejecutable
        exe_name = "SelectorDeContexto.exe" if sys.platform == "win32" else "SelectorDeContexto"
        exe_path = os.path.join("dist", exe_name)
        print(f"Ejecutable ubicado en: {os.path.abspath(exe_path)}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el ejecutable: {e}")
        return 1
    finally:
        # Limpiar archivos temporales
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
