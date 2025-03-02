#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestión de temas y estilos visuales para la aplicación.
"""
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Clase para gestionar los temas de la aplicación."""
    
    def __init__(self):
        """Inicializa el gestor de temas."""
        self.current_theme = "light"
    
    def get_theme_colors(self, theme_name=None):
        """
        Obtiene los colores para un tema específico.
        
        Args:
            theme_name (str, optional): Nombre del tema. Si es None, se usa el tema actual.
            
        Returns:
            dict: Diccionario con los colores del tema
        """
        theme = theme_name or self.current_theme
        
        if theme == "dark":
            return {
                # Colores generales
                'bg_color': "#282828",         # Fondo principal
                'fg_color': "#E0E0E0",         # Texto normal
                'secondary_bg': "#3A3D41",     # Fondo secundario
                'accent_color': "#0078D7",     # Color de acento
                
                # Colores específicos de widgets
                'tree_bg': "#252525",          # Fondo del árbol
                'tree_fg': "#E0E0E0",          # Texto del árbol
                'content_bg': "#1E1E1E",       # Fondo del área de código
                'content_fg': "#F8F8F8",       # Texto del área de código
                'selection_bg': "#264F78",     # Fondo de selección
                'selection_fg': "#FFFFFF",     # Texto de selección
                'highlight_bg': "#3A3A35",     # Fondo de resaltado
                'button_bg': "#3F3F3F",        # Fondo de botones
                'button_fg': "#E0E0E0",        # Texto de botones
                'button_active': "#505050",    # Fondo de botón activo
                'frame_bg': "#1E1E1E",         # Fondo de marcos
                'border_color': "#3F3F3F",     # Color de bordes
                
                # Colores para etiquetas
                'header_color': "#77AAFF",     # Color de encabezados
                'file_header_color': "#5599FF",# Color de encabezado de archivo
                'complete_file_color': "#22BB22", # Color para archivo completo
                'selection_header_color': "#77AAFF", # Color para encabezado de selección
            }
        else:  # Light theme (default)
            return {
                # Colores generales
                'bg_color': "#F8F8F8",         # Fondo principal
                'fg_color': "#333333",         # Texto normal
                'secondary_bg': "#EAEAEA",     # Fondo secundario
                'accent_color': "#0078D7",     # Color de acento
                
                # Colores específicos de widgets
                'tree_bg': "#FFFFFF",          # Fondo del árbol
                'tree_fg': "#333333",          # Texto del árbol
                'content_bg': "#FFFFFF",       # Fondo del área de código
                'content_fg': "#000000",       # Texto del área de código
                'selection_bg': "#ADD6FF",     # Fondo de selección
                'selection_fg': "#000000",     # Texto de selección
                'highlight_bg': "#FFFF99",     # Fondo de resaltado
                'button_bg': "#F0F0F0",        # Fondo de botones
                'button_fg': "#333333",        # Texto de botones
                'button_active': "#E5E5E5",    # Fondo de botón activo
                'frame_bg': "#F0F0F0",         # Fondo de marcos
                'border_color': "#DDDDDD",     # Color de bordes
                
                # Colores para etiquetas
                'header_color': "#0066CC",     # Color de encabezados
                'file_header_color': "#0066CC",# Color de encabezado de archivo
                'complete_file_color': "#008000", # Color para archivo completo
                'selection_header_color': "#0066CC", # Color para encabezado de selección
            }
    
    def set_theme(self, theme_name):
        """
        Configura el tema actual.
        
        Args:
            theme_name (str): Nombre del tema a configurar ('light' o 'dark')
        """
        if theme_name in ["light", "dark"]:
            self.current_theme = theme_name
    
    def apply_theme(self, root):
        """
        Aplica el tema actual a la aplicación.
        
        Args:
            root: Ventana raíz de la aplicación
        """
        colors = self.get_theme_colors()
        style = ttk.Style()
        
        # Usar 'clam' como tema base ya que es uno de los más personalizables
        style.theme_use("clam")
        
        # Configuración general
        style.configure(".", 
                    background=colors['bg_color'], 
                    foreground=colors['fg_color'], 
                    bordercolor=colors['border_color'],
                    focuscolor=colors['accent_color'])
        
        # Frames con bordes suaves
        style.configure("TFrame", 
                    background=colors['frame_bg'], 
                    borderwidth=0)
        
        # LabelFrames con bordes redondeados
        style.configure("TLabelFrame", 
                    background=colors['frame_bg'], 
                    borderwidth=1, 
                    relief="groove")
        
        style.configure("TLabelFrame.Label", 
                    background=colors['frame_bg'], 
                    foreground=colors['fg_color'],
                    font=("Segoe UI", 9, "normal"))
        
        # Botones más modernos
        style.configure("TButton", 
                    background=colors['button_bg'], 
                    foreground=colors['button_fg'], 
                    relief="flat",
                    borderwidth=1,
                    padding=(8, 4),
                    font=("Segoe UI", 9, "normal"))
        
        # Efecto hover para botones
        style.map("TButton",
                background=[("active", colors['accent_color']), ("pressed", colors['accent_color'])],
                foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")],
                relief=[("active", "flat"), ("pressed", "flat")])
        
        # Configurar el Panedwindow para que sea más moderno
        style.configure("TPanedwindow", 
                    background=colors['bg_color'])
        
        # Configurar separadores de paneles
        style.configure("Sash", 
                    background="#CCCCCC",
                    sashthickness=4)
        
        # Treeview con estilo minimalista
        style.configure("Treeview", 
                    background=colors['tree_bg'], 
                    foreground=colors['tree_fg'], 
                    fieldbackground=colors['tree_bg'], 
                    bordercolor=colors['border_color'],
                    borderwidth=0,
                    font=("Segoe UI", 9, "normal"))
        
        style.configure("Treeview.Heading", 
                    background=colors['frame_bg'],
                    foreground=colors['fg_color'],
                    borderwidth=1,
                    relief="flat",
                    font=("Segoe UI", 9, "bold"))
        
        style.map("Treeview", 
                background=[("selected", colors['selection_bg'])],
                foreground=[("selected", colors['selection_fg'])])
        
        # Scrollbars minimalistas
        style.configure("TScrollbar",
                    background=colors['bg_color'],
                    bordercolor=colors['bg_color'],
                    arrowcolor=colors['button_fg'],
                    troughcolor=colors['frame_bg'],
                    relief="flat",
                    borderwidth=0)
        
        style.map("TScrollbar",
                background=[("active", colors['button_bg']), ("disabled", colors['bg_color'])],
                arrowcolor=[("active", colors['accent_color']), ("disabled", colors['button_fg'])])
        
        # Aplicar a la ventana principal
        root.configure(background=colors['bg_color'])
        
        return colors
