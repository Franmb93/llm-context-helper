#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Selector de Contexto para LLMs.
"""

import os
import sys

# Añadir el directorio raíz al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.app import ContextSelectorApp
from src.utils.logger import configure_logging
from src.utils.file_utils import ensure_directory_exists

def ensure_assets_directory():
    """Crea la carpeta de assets si no existe y otros recursos necesarios."""
    # Determinar ruta a la carpeta assets
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    
    # Crear la carpeta si no existe
    ensure_directory_exists(assets_dir)
    
    # Verificar si existe el ícono
    icon_path = os.path.join(assets_dir, "icon.ico")
    if not os.path.exists(icon_path):
        # Si no hay ícono, podríamos crear uno básico o usar un valor por defecto
        pass
    
    return assets_dir

def main():
    """Función principal que inicia la aplicación."""
    # Configurar logging
    logger = configure_logging()
    
    try:
        # Asegurar que exista la carpeta de assets
        ensure_assets_directory()
        
        # Iniciar la aplicación
        app = ContextSelectorApp()
        app.mainloop()
    except Exception as e:
        logger.exception(f"Error no manejado: {str(e)}")
        raise

if __name__ == "__main__":
    main()
