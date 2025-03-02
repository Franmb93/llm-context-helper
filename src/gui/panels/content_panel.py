#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel para visualizar el contenido de los archivos con resaltado de sintaxis.
"""
import os
import tkinter as tk
from tkinter import ttk

from gui.panels.base_panel import Panel

class FileContentPanel(Panel):
    """Panel para mostrar el contenido de archivos con resaltado de sintaxis."""
    
    def __init__(self, parent, syntax_highlighter, on_add_selection, on_context_menu):
        """
        Inicializa el panel de contenido de archivos.
        
        Args:
            parent: Widget padre
            syntax_highlighter: Instancia de SyntaxHighlighter
            on_add_selection: Callback al añadir una selección
            on_context_menu: Callback para mostrar el menú contextual
        """
        self.syntax_highlighter = syntax_highlighter
        self.on_add_selection = on_add_selection
        self.on_context_menu = on_context_menu
        self.current_file = None
        self.highlight_tag = "selection_highlight"
        super().__init__(parent)
    
    def _create_widgets(self):
        """Crea los widgets del panel de contenido."""
        self.frame = ttk.LabelFrame(self.parent, text="Contenido del archivo", padding=(8, 5, 8, 8))
        
        # Determinar el tema actual para configurar los colores adecuados
        try:
            app_settings_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "app_settings.json")
            theme = "light"  # default
            if os.path.exists(app_settings_file):
                with open(app_settings_file, 'r') as f:
                    import json
                    app_settings = json.load(f)
                    if 'general' in app_settings and 'theme' in app_settings['general']:
                        theme = app_settings['general']['theme']
        except Exception:
            theme = "light"  # en caso de error, usar tema claro
        
        # Configurar colores basados en el tema
        if theme == "dark":
            bg_color = "#383838"
            fg_color = "#FFFFFF"
            selection_bg = "#505050"
            selection_fg = "#FFFFFF"
            highlight_bg = "#3A3A35"  # Amarillo oscuro
        else:
            bg_color = "#FFFFFF"
            fg_color = "#000000"
            selection_bg = "#0078D7"
            selection_fg = "#FFFFFF"
            highlight_bg = "#FFFF99"  # Amarillo claro
        
        # Crear widget Text con scrollbars
        self.content_scrolly = ttk.Scrollbar(self.frame)
        self.content_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_scrollx = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.content_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.content_text = tk.Text(
            self.frame,
            wrap=tk.NONE,
            yscrollcommand=self.content_scrolly.set,
            xscrollcommand=self.content_scrollx.set,
            font=("Courier New", 10),
            state=tk.DISABLED,
            background=bg_color,
            foreground=fg_color,
            insertbackground=fg_color,
            selectbackground=selection_bg,
            selectforeground=selection_fg
        )
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.content_scrolly.config(command=self.content_text.yview)
        self.content_scrollx.config(command=self.content_text.xview)
        
        # Configurar tag para resaltado de selecciones
        self.content_text.tag_configure(
            self.highlight_tag,
            background=highlight_bg
        )
        
        # Botón para añadir selección al contexto con estilo moderno
        self.selection_frame = ttk.Frame(self.frame, padding=(0, 5, 0, 0))
        self.selection_frame.pack(fill=tk.X, padx=5, pady=5)

        
        # Menú contextual
        self.content_menu = tk.Menu(self.content_text, tearoff=0)
        self.content_menu.add_command(
            label="Añadir selección al contexto",
            command=self._handle_add_selection
        )
        self.content_menu.add_command(
            label="Copiar", 
            command=self._copy_selection
        )
        
        # Vincular el menú contextual
        self.content_text.bind("<Button-3>", self._handle_context_menu)
        

        
        # Crear estilo para el botón de selección
        style = ttk.Style()
        style.configure("Selection.TButton", 
                         font=("Segoe UI", 9, "normal"))
        
        self.add_selection_btn = ttk.Button(
            self.selection_frame, 
            text="Añadir selección al contexto", 
            command=self._handle_add_selection,
            style="Selection.TButton"
        )
        self.add_selection_btn.pack(side=tk.LEFT, padx=5)
    
    def load_file(self, file_path):
        """
        Carga el contenido de un archivo en el widget Text.
        
        Args:
            file_path (str): Ruta del archivo a cargar
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            self.current_file = file_path
            
            # Actualizar el widget Text
            self.content_text.config(state=tk.NORMAL)
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, content)
            
            # Aplicar resaltado de sintaxis según extensión
            file_ext = os.path.splitext(file_path)[1].lower()
            self.syntax_highlighter.highlight(self.content_text, file_ext)
            
            self.content_text.config(state=tk.DISABLED)
            
            # Actualizar título del frame
            self.frame.config(text=f"Contenido: {os.path.basename(file_path)}")
            
            return True
        except Exception as e:
            print(f"Error al cargar archivo: {str(e)}")
            return False
    
    def _handle_add_selection(self):
        """Maneja el evento de añadir selección."""
        if self.on_add_selection:
            self.on_add_selection(self.content_text)
    
    def _handle_context_menu(self, event):
        """Muestra el menú contextual."""
        if self.on_context_menu:
            self.on_context_menu(event, self.content_text, self.content_menu)
    
    def _copy_selection(self):
        """Copia la selección actual al portapapeles."""
        try:
            selection = self.content_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selection:
                self.parent.clipboard_clear()
                self.parent.clipboard_append(selection)
                self.parent.update()
        except tk.TclError:
            pass  # No hay selección
    
    def highlight_selection(self, start_pos, end_pos):
        """
        Aplica resaltado visual a una región seleccionada.
        
        Args:
            start_pos: Posición de inicio
            end_pos: Posición de fin
        """
        self.content_text.tag_add(self.highlight_tag, start_pos, end_pos)
        self.content_text.tag_configure(
            self.highlight_tag, 
            background="#FFFF99",  # Amarillo claro
            borderwidth=0
        )
    
    def clear_highlights(self):
        """Limpia todos los resaltados visuales."""
        self.content_text.config(state=tk.NORMAL)
        self.content_text.tag_remove(self.highlight_tag, "1.0", tk.END)
        self.content_text.config(state=tk.DISABLED)
    
    def apply_highlights(self, ranges):
        """
        Aplica resaltado a los rangos especificados.
        
        Args:
            ranges (list): Lista de tuplas (inicio, fin)
        """
        self.content_text.config(state=tk.NORMAL)
        for start_pos, end_pos in ranges:
            self.highlight_selection(start_pos, end_pos)
        self.content_text.config(state=tk.DISABLED)
