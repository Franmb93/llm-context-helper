#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Selector de Contexto para LLMs.
"""

import os
import sys
from context_selector import ContextSelector
from logger import configure_logging

def main():
    """Función principal que inicia la aplicación."""
    # Configurar logging
    logger = configure_logging()
    
    try:
        # Iniciar la aplicación
        app = ContextSelector()
        app.mainloop()
    except Exception as e:
        logger.exception(f"Error no manejado: {str(e)}")
        raise

if __name__ == "__main__":
    main()