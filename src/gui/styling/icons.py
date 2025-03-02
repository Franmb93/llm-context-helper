#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestión de iconos para la aplicación.
"""
import tkinter as tk

class IconManager:
    """Clase para gestionar los íconos de la aplicación."""
    
    def __init__(self, theme_manager=None):
        """
        Inicializa el gestor de íconos.
        
        Args:
            theme_manager: Instancia de ThemeManager para obtener colores de tema
        """
        self.theme_manager = theme_manager
        self.icons = {}
        self.create_icons()
    
    def create_icons(self):
        """Crea los íconos básicos para la aplicación."""
        # Obtener colores según el tema actual
        colors = {}
        if self.theme_manager:
            colors = self.theme_manager.get_theme_colors()
        else:
            # Colores predeterminados si no hay theme_manager
            colors = {
                'bg_color': "#F8F8F8",
                'fg_color': "#333333",
            }
        
        # Definir colores para los diferentes tipos de archivos
        icon_colors = {
            "directory": "#FFD700",  # Dorado para carpetas
            "file": "#A9A9A9",       # Gris para archivos genéricos
            "python": "#3776AB",     # Azul Python
            "javascript": "#F7DF1E", # Amarillo JavaScript
            "html": "#E34F26",       # Naranja HTML
            "css": "#1572B6",        # Azul CSS
            "markdown": "#083FA1",   # Azul oscuro Markdown
            "json": "#000000",       # Negro JSON
            "xml": "#F16529",        # Naranja XML
            "text": "#696969",       # Gris oscuro texto
        }
        
        # Crear un icono simple para cada tipo
        for icon_name, color in icon_colors.items():
            icon = tk.PhotoImage(width=16, height=16)
            
            # Dibujar un rectángulo o círculo coloreado
            for y in range(16):
                for x in range(16):
                    # Carpetas: rectángulo con "pestaña"
                    if icon_name == "directory":
                        if (2 <= x <= 14 and 4 <= y <= 14) or (5 <= x <= 11 and 2 <= y <= 4):
                            icon.put(color, (x, y))
                    # Archivos: rectángulo simple con "doblez" en la esquina
                    else:
                        if 2 <= x <= 14 and 2 <= y <= 14:
                            if x >= 10 and y <= 6 and x + y <= 16:
                                icon.put("#FFFFFF", (x, y))  # Doblez blanco
                            else:
                                icon.put(color, (x, y))
            
            self.icons[icon_name] = icon
    
    def update_icons(self):
        """Actualiza los íconos según el tema actual."""
        if self.theme_manager:
            # Volver a crear los íconos con los colores actualizados
            self.create_icons()
    
    def get_icon(self, icon_name):
        """
        Obtiene un ícono por su nombre.
        
        Args:
            icon_name (str): Nombre del ícono
            
        Returns:
            tk.PhotoImage: Ícono solicitado o ícono genérico si no existe
        """
        return self.icons.get(icon_name, self.icons.get("file"))
    
    def get_file_icon(self, file_extension):
        """
        Obtiene el ícono adecuado para un tipo de archivo según su extensión.
        
        Args:
            file_extension (str): Extensión del archivo (con o sin punto)
            
        Returns:
            tk.PhotoImage: Ícono correspondiente
        """
        # Normalizar la extensión
        ext = file_extension.lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        
        # Mapeo de extensiones a íconos
        extension_to_icon = {
            '.py': 'python',
            '.pyw': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.scss': 'css',
            '.sass': 'css',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.json': 'json',
            '.xml': 'xml',
            '.svg': 'xml',
            '.txt': 'text',
        }
        
        icon_name = extension_to_icon.get(ext, "file")
        return self.get_icon(icon_name)
