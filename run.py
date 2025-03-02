#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar directamente el Selector de Contexto sin generar un ejecutable.
"""

import os
import sys

def main():
    """Función principal para ejecutar la aplicación."""
    print("Iniciando Selector de Contexto para LLMs...")
    
    # Añadir el directorio raíz al path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Corregir primero las importaciones relativas
    fix_imports_script = os.path.join(project_dir, "installers", "fix_imports.py")
    
    if os.path.exists(fix_imports_script):
        print("Corrigiendo importaciones relativas...")
        import subprocess
        subprocess.run([sys.executable, fix_imports_script], check=True)
    
    # Importar y ejecutar la aplicación
    try:
        from src.core.app import ContextSelectorApp
        
        app = ContextSelectorApp()
        app.mainloop()
    except ImportError as e:
        print(f"Error al importar la aplicación: {e}")
        print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto.")
        return 1
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
