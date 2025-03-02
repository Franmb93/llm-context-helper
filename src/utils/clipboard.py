#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para el manejo del portapapeles.
"""

def copy_to_clipboard(root, text):
    """
    Copia texto al portapapeles.
    
    Args:
        root: Instancia de Tkinter (ventana)
        text (str): Texto a copiar
        
    Returns:
        bool: True si se copió correctamente
    """
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Necesario para que el texto permanezca después de que el programa termine
        return True
    except Exception as e:
        print(f"Error al copiar al portapapeles: {str(e)}")
        return False
