#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel para visualizar y gestionar el contexto seleccionado.
"""
import os
import tkinter as tk
from tkinter import ttk

from gui.panels.base_panel import Panel

class ContextPanel(Panel):
    """Panel para mostrar y gestionar el contexto seleccionado."""
    
    def __init__(self, parent, on_copy, on_save, on_clear, on_context_menu, on_stats):
        """
        Inicializa el panel de contexto.
        
        Args:
            parent: Widget padre
            on_copy: Callback para copiar contexto
            on_save: Callback para guardar contexto
            on_clear: Callback para limpiar contexto
            on_context_menu: Callback para menú contextual
            on_stats: Callback para mostrar estadísticas
        """
        self.on_copy = on_copy
        self.on_save = on_save
        self.on_clear = on_clear
        self.on_context_menu = on_context_menu
        self.on_stats = on_stats
        self.context_selection_markers = {}
        self.remove_handler = None
        super().__init__(parent)
    
    def _create_widgets(self):
        """Crea los widgets del panel de contexto."""
        self.frame = ttk.LabelFrame(self.parent, text="Contexto seleccionado", padding=(8, 5, 8, 8))
        
        # Botones para el contexto con estilo moderno
        self.btn_frame = ttk.Frame(self.frame, padding=(0, 0, 0, 5))
        self.btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Crear estilo para botones de contexto
        style = ttk.Style()
        style.configure("Context.TButton", 
                         font=("Segoe UI", 9, "normal"))
        
        # Botones con estilo moderno, más pequeños y mejor organizados
        button_padding = (8, 2)  # (x, y) padding para botones
        
        self.copy_btn = ttk.Button(
            self.btn_frame, 
            text="Copiar", 
            command=self._handle_copy,
            style="Context.TButton",
            padding=button_padding
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(
            self.btn_frame, 
            text="Guardar", 
            command=self._handle_save,
            style="Context.TButton",
            padding=button_padding
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_btn = ttk.Button(
            self.btn_frame,
            text="Estadísticas",
            command=self._handle_stats,
            style="Context.TButton",
            padding=button_padding
        )
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            self.btn_frame, 
            text="Limpiar",
            command=self._handle_clear,
            style="Context.TButton",
            padding=button_padding
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
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
            green_color = "#00FF00"  # Verde más brillante para oscuridad
            blue_color = "#5599FF"   # Azul más brillante para oscuridad
            selection_bg = "#505050"
            selection_fg = "#FFFFFF"
            highlight_bg = "#5A5A15"  # Amarillo oscuro
        else:
            bg_color = "#FFFFFF"
            fg_color = "#000000"
            green_color = "#008000"  # Verde estándar
            blue_color = "#0000FF"   # Azul estándar
            selection_bg = "#0078D7"
            selection_fg = "#FFFFFF"
            highlight_bg = "#FFFF99"  # Amarillo claro
        
        # Crear widget Text para el contexto con scrollbars
        self.context_scrolly = ttk.Scrollbar(self.frame)
        self.context_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.context_scrollx = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.context_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.context_text = tk.Text(
            self.frame,
            wrap=tk.NONE,
            yscrollcommand=self.context_scrolly.set,
            xscrollcommand=self.context_scrollx.set,
            font=("Courier New", 10),
            background=bg_color,
            foreground=fg_color,
            insertbackground=fg_color,
            selectbackground=selection_bg,
            selectforeground=selection_fg
        )
        self.context_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.context_scrolly.config(command=self.context_text.yview)
        self.context_scrollx.config(command=self.context_text.xview)
        
        # Configurar tags para el formato con colores que respeten el tema
        self.context_text.tag_configure("file_header", font=("TkDefaultFont", 10, "bold"))
        self.context_text.tag_configure("complete_file", font=("TkDefaultFont", 9, "italic"), foreground=green_color)
        self.context_text.tag_configure("selection_header", font=("TkDefaultFont", 9, "italic"), foreground=blue_color)
        self.context_text.tag_configure("selection_highlight", background=highlight_bg)
        
        # Menú contextual para el área de contexto
        self.context_menu = tk.Menu(self.context_text, tearoff=0)
        self.context_menu.add_command(label="Eliminar selección", command=self._handle_remove_selected)
        
        # Vincular eventos
        self.context_text.bind("<Button-3>", self._show_context_menu)
    
    def _handle_stats(self):
        """Maneja el evento de mostrar estadísticas del contexto."""
        if self.on_stats:
            self.on_stats()
    
    def _handle_copy(self):
        """Maneja el evento de copiar contexto."""
        if self.on_copy:
            self.on_copy()
    
    def _handle_save(self):
        """Maneja el evento de guardar contexto."""
        if self.on_save:
            self.on_save()
    
    def _handle_clear(self):
        """Maneja el evento de limpiar contexto."""
        if self.on_clear:
            self.on_clear()
    
    def _handle_remove_selected(self):
        """Maneja el evento de eliminar selección."""
        if self.remove_handler:
            self.remove_handler()
    
    def _show_context_menu(self, event):
        """Muestra el menú contextual."""
        if self.on_context_menu:
            self.on_context_menu(event, self.context_text, self.context_menu)
    
    def update_context(self, selections):
        """
        Actualiza la visualización del contexto.
        
        Args:
            selections (dict): Diccionario con las selecciones
        """
        # Importar os si necesario (alternativa mejor: asegurar que está importado arriba)
        import os
        
        self.context_text.config(state=tk.NORMAL)
        self.context_text.delete(1.0, tk.END)
        
        # Reiniciar los marcadores
        self.context_selection_markers = {}
        
        for file_path, file_selections in selections.items():
            if file_selections:
                file_name = os.path.basename(file_path)
                
                # Mostrar encabezado para el archivo
                self.context_text.insert(tk.END, f"--- {file_name} ---\n", "file_header")
                
                # Procesar cada selección
                has_whole_file = False
                
                for i, (selection, is_whole_file) in enumerate(file_selections):
                    if is_whole_file:
                        has_whole_file = True
                        self.context_text.insert(tk.END, "Archivo completo incluido\n\n", "complete_file")
                        
                        # Guardar posición de inicio para el marcador
                        start_pos = self.context_text.index(tk.END)
                        
                        self.context_text.insert(tk.END, selection + "\n\n")
                        
                        # Guardar posición final
                        end_pos = self.context_text.index(tk.END)
                        
                        # Almacenar marcadores de posición para esta selección
                        if file_path not in self.context_selection_markers:
                            self.context_selection_markers[file_path] = []
                        
                        # Guardar tupla con (índice, inicio, fin, es_archivo_completo)
                        self.context_selection_markers[file_path].append((0, start_pos, end_pos, True))
                        
                        break  # Si hay un archivo completo, solo mostramos ese
                
                # Si no hay archivo completo, mostrar selecciones individuales
                if not has_whole_file:
                    for i, (selection, _) in enumerate(file_selections):
                        selection_header = f"Selección {i+1}:\n"
                        self.context_text.insert(tk.END, selection_header, "selection_header")
                        
                        # Guardar posición de inicio
                        start_pos = self.context_text.index(tk.END)
                        
                        self.context_text.insert(tk.END, selection + "\n\n")
                        
                        # Guardar posición final
                        end_pos = self.context_text.index(tk.END)
                        
                        # Almacenar marcadores
                        if file_path not in self.context_selection_markers:
                            self.context_selection_markers[file_path] = []
                        
                        # Guardar tupla
                        self.context_selection_markers[file_path].append((i, start_pos, end_pos, False))
        
        self.context_text.config(state=tk.DISABLED)
        
    def set_remove_handler(self, handler):
        """
        Establece el controlador para eliminar selecciones.
        
        Args:
            handler: Función a llamar cuando se elimina una selección
        """
        self.remove_handler = handler
        self.context_menu.entryconfig(
            self.context_menu.index("Eliminar selección"),
            command=handler
        )
