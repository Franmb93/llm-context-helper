#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Selector de Contexto para LLMs.
"""

import os
import sys
from context_selector import ContextSelector

from logger import configure_logging

def ensure_assets_directory():
    """Crea la carpeta de assets si no existe y genera un ícono básico si es necesario."""
    # Determinar ruta a la carpeta assets
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    
    # Crear la carpeta si no existe
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
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
        app = ContextSelector()
        app.mainloop()
    except Exception as e:
        logger.exception(f"Error no manejado: {str(e)}")
        raise

if __name__ == "__main__":
    main()