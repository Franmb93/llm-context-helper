#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades generales para el Selector de Contexto.
"""

import os
import tkinter as tk
from tkinter import messagebox

def copy_to_clipboard(root, text):
    """
    Copia texto al portapapeles.
    
    Args:
        root (tk.Tk): Raíz de la aplicación Tkinter
        text (str): Texto a copiar al portapapeles
    """
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Necesario para que permanezca en el portapapeles

def save_to_file(content, file_path):
    """
    Guarda texto en un archivo.
    
    Args:
        content (str): Contenido a guardar
        file_path (str): Ruta del archivo donde guardar
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Guardar el contenido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudo guardar el archivo: {str(e)}")
        return False

def format_file_size(size_bytes):
    """
    Formatea un tamaño en bytes a una representación legible.
    
    Args:
        size_bytes (int): Tamaño en bytes
    
    Returns:
        str: Tamaño formateado (e.j. "4.2 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def get_file_icon(file_ext):
    """
    Devuelve un carácter de ícono para representar un tipo de archivo.
    Función básica que devuelve un emoji o carácter Unicode según la extensión.
    
    Args:
        file_ext (str): Extensión del archivo
    
    Returns:
        str: Carácter que representa el tipo de archivo
    """
    # Mapeo de extensiones a iconos (usando emojis o caracteres Unicode básicos)
    icons = {
        # Código y scripting
        '.py': '🐍',   # Python
        '.js': '📜',   # JavaScript
        '.html': '🌐',  # HTML
        '.css': '🎨',   # CSS
        '.java': '☕',  # Java
        '.cpp': '🔧',   # C++
        '.c': '🔧',     # C
        '.h': '📄',     # C/C++ Header
        '.cs': '🔷',    # C#
        '.php': '🐘',   # PHP
        '.rb': '💎',    # Ruby
        '.go': '🔹',    # Go
        '.rs': '⚙️',    # Rust
        '.ts': '📘',    # TypeScript
        '.swift': '🔶', # Swift
        '.kt': '🧩',    # Kotlin
        
        # Documentos y datos
        '.md': '📝',    # Markdown
        '.txt': '📄',   # Texto plano
        '.json': '📊',  # JSON
        '.xml': '📊',   # XML
        '.yml': '📋',   # YAML
        '.yaml': '📋',  # YAML
        '.csv': '📊',   # CSV
        '.sql': '🗄️',   # SQL
        
        # Otros
        '.sh': '💻',    # Shell script
        '.bat': '💻',   # Batch script
        '.ps1': '💻',   # PowerShell
    }
    
    return icons.get(file_ext.lower(), '📄')  # Ícono por defecto para archivos no reconocidos

def create_dir_if_not_exists(directory):
    """
    Crea un directorio si no existe.
    
    Args:
        directory (str): Ruta del directorio a crear
    
    Returns:
        bool: True si se creó correctamente o ya existía, False en caso de error
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        print(f"Error al crear directorio {directory}: {str(e)}")
        return False

def create_custom_scroll_event(root):
    """
    Crea un evento virtual personalizado para notificar cambios de desplazamiento.
    
    Args:
        root: Instancia raíz de Tk
    """
    root.event_add('<<Scroll>>', '<B1-Motion>', '<MouseWheel>', '<Button-4>', '<Button-5>')
    return '<<Scroll>>'