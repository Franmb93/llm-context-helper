#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar un ejecutable del Selector de Contexto utilizando PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import platform

def main():
    """Función principal para generar el ejecutable."""
    print("Generando ejecutable para el Selector de Contexto para LLMs...")
    
    # Asegurarse de que el directorio está limpio
    if os.path.exists("dist"):
        print("Limpiando directorio dist anterior...")
        shutil.rmtree("dist")
    
    if os.path.exists("build"):
        print("Limpiando directorio build anterior...")
        shutil.rmtree("build")
    
    # Determinar si estamos en Windows
    is_windows = platform.system() == "Windows"
    
    # Obtener la ruta del icono
    icon_path = os.path.join("assets", "icon.ico")
    if not os.path.exists(icon_path):
        print("Advertencia: No se encuentra el icono. Se utilizará un icono por defecto.")
        icon_path = None
    
    # Variable para la ruta de PyInstaller
    pyinstaller_exe = "pyinstaller"  # Por defecto, buscar en PATH
    
    # Construir los argumentos para PyInstaller
    pyinstaller_args = [
        pyinstaller_exe,  # Usar la variable en lugar de string literal
        "--name=SelectorDeContexto",
        "--onefile",
        "--windowed",  # Sin consola
        "--clean",
    ]
    
    # Añadir icono si existe
    if icon_path:
        pyinstaller_args.append(f"--icon={icon_path}")
    
    # Añadir el script principal
    pyinstaller_args.append("src/main.py")
    
    # Añadir recursos adicionales
    pyinstaller_args.extend([
        "--add-data", f"assets{os.pathsep}assets",
        "--add-data", f"config{os.pathsep}config",
        "--add-data", f"resources{os.pathsep}resources",
    ])
    
    # Ejecutar PyInstaller
    print("Ejecutando "C:\Users\Corhl\AppData\Roaming\Python\Python312\Scripts\pyinstaller.exe" con los siguientes argumentos:")
    print(" ".join(pyinstaller_args))
    
    try:
        subprocess.run(pyinstaller_args, check=True)
        
        print("\n¡Ejecutable generado correctamente!")
        
        # Mostrar ubicación del ejecutable
        exe_name = "SelectorDeContexto.exe" if is_windows else "SelectorDeContexto"
        exe_path = os.path.join("dist", exe_name)
        print(f"Ejecutable ubicado en: {os.path.abspath(exe_path)}")
        
        # Instrucciones adicionales
        print("\nInstrucciones:")
        print("1. Haz doble clic en el ejecutable para iniciar la aplicación")
        print("2. Para distribución, puedes comprimir la carpeta 'dist' y compartirla")
        
        if is_windows:
            print("\nNota para Windows: Puedes crear un acceso directo en el escritorio para facilitar el acceso")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el ejecutable: {e}")
        print("Asegúrate de tener "C:\Users\Corhl\AppData\Roaming\Python\Python312\Scripts\pyinstaller.exe" instalado con: pip install pyinstaller")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
