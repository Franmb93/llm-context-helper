#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de configuración de logging para la aplicación.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

def configure_logging():
    """
    Configura el logging de la aplicación.
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear logger
    logger = logging.getLogger('ContextSelector')
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicar handlers si se llama varias veces
    if logger.handlers:
        return logger
    
    # Crear directorio de logs si no existe
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Formato de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Nombre del archivo de log con fecha
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(logs_dir, f'context_selector_{current_date}.log')
    
    # Handler para archivo con rotación (máximo 5 archivos de 1MB)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("Logging configurado correctamente")
    
    return logger
