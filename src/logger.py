#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de logging para diagnóstico de problemas.
"""

import os
import logging
from datetime import datetime

def configure_logging(log_level=logging.INFO):
    """
    Configura el sistema de logging.
    
    Args:
        log_level: Nivel de logging (default: INFO)
    """
    # Crear directorio para logs si no existe
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log con fecha y hora
    log_file = os.path.join(log_dir, f"context_selector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Configurar logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Crear logger
    logger = logging.getLogger("context_selector")
    logger.info("Iniciando Selector de Contexto")
    
    return logger