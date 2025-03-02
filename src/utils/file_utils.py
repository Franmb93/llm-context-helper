#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para operaciones con archivos.
"""
import os
import tkinter as tk

def save_to_file(content, file_path):
    """
    Guarda texto en un archivo.
    
    Args:
        content (str): Contenido a guardar
        file_path (str): Ruta del archivo
        
    Returns:
        bool: True si se guardó correctamente
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error al guardar en archivo: {str(e)}")
        return False

def ensure_directory_exists(directory):
    """
    Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        directory (str): Ruta del directorio
        
    Returns:
        bool: True si el directorio existe o se creó correctamente
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        print(f"Error al crear directorio: {str(e)}")
        return False

def get_file_extension(file_path):
    """
    Obtiene la extensión de un archivo.
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        str: Extensión del archivo (con punto)
    """
    return os.path.splitext(file_path)[1].lower()

def get_file_name(file_path):
    """
    Obtiene el nombre de un archivo sin ruta.
    
    Args:
        file_path (str): Ruta del archivo
        
    Returns:
        str: Nombre del archivo
    """
    return os.path.basename(file_path)

def create_custom_scroll_event(root):
    """
    Crea eventos personalizados para el desplazamiento con la rueda del ratón.
    
    Args:
        root: Instancia de Tkinter (ventana)
    """
    def on_mouse_wheel(event):
        # Determinar la dirección del desplazamiento
        if event.num == 4 or event.delta > 0:  # Desplazamiento hacia arriba
            delta = -1
        elif event.num == 5 or event.delta < 0:  # Desplazamiento hacia abajo
            delta = 1
        else:
            return
        
        # Obtener el widget bajo el cursor
        widget = event.widget
        
        # Aplicar desplazamiento si el widget es un Text o Canvas
        if isinstance(widget, (tk.Text, tk.Canvas)):
            widget.yview_scroll(delta, "units")
        
        return "break"  # Evitar propagación del evento
    
    # Vincular eventos para diferentes sistemas
    root.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows
    root.bind_all("<Button-4>", on_mouse_wheel)    # Linux - rueda arriba
    root.bind_all("<Button-5>", on_mouse_wheel)    # Linux - rueda abajo
