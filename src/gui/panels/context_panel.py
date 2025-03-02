#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel para visualizar y gestionar el contexto seleccionado.
"""
import os
import tkinter as tk
from tkinter import ttk

from src.gui.panels.base_panel import Panel

class ContextPanel(Panel):
    """Panel para mostrar y gestionar el contexto seleccionado."""
    
    def __init__(self, parent, on_copy, on_save, on_clear, on_context_menu, on_stats, on_instructions=None):
        """
        Inicializa el panel de contexto.
        
        Args:
            parent: Widget padre
            on_copy: Callback para copiar contexto
            on_save: Callback para guardar contexto
            on_clear: Callback para limpiar contexto
            on_context_menu: Callback para menú contextual
            on_stats: Callback para mostrar estadísticas
            on_instructions: Callback para gestionar instrucciones
        """
        self.on_copy = on_copy
        self.on_save = on_save
        self.on_clear = on_clear
        self.on_context_menu = on_context_menu
        self.on_stats = on_stats
        self.on_instructions = on_instructions
        self.context_selection_markers = {}
        self.remove_handler = None
        self.instruction_manager = None
        super().__init__(parent)
    
    def _create_widgets(self):
        """Crea los widgets del panel de contexto."""
        self.frame = ttk.LabelFrame(self.parent, text="Contexto seleccionado", padding=(8, 5, 8, 8))
        
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
            combobox_bg = "#555555"
            combobox_fg = "#FFFFFF"
            button_bg = "#444444"
        else:
            bg_color = "#FFFFFF"
            fg_color = "#000000"
            green_color = "#008000"  # Verde estándar
            blue_color = "#0000FF"   # Azul estándar
            selection_bg = "#0078D7"
            selection_fg = "#FFFFFF"
            highlight_bg = "#FFFF99"  # Amarillo claro
            combobox_bg = "#FFFFFF"
            combobox_fg = "#000000"
            button_bg = "#F0F0F0"
        
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
        
        # Botón para instrucciones extra
        self.instructions_btn = ttk.Button(
            self.btn_frame,
            text="Instrucciones",
            command=self._handle_instructions,
            style="Context.TButton",
            padding=button_padding
        )
        self.instructions_btn.pack(side=tk.LEFT, padx=5)
        
        # Variable para almacenar la instrucción seleccionada
        self.instruction_var = tk.StringVar()
        self.instruction_var.set("Sin instrucción")
        
        # Frame para instrucción
        instr_frame = ttk.Frame(self.btn_frame)
        instr_frame.pack(side=tk.LEFT, padx=5)
        
        # Usar un OptionMenu en lugar de Combobox
        self.instruction_menu = tk.OptionMenu(
            instr_frame,
            self.instruction_var,
            "Sin instrucción"
        )
        
        # Configurar colores del OptionMenu según el tema
        if theme == "dark":
            self.instruction_menu.config(
                background=button_bg,
                foreground=combobox_fg,
                activebackground="#666666",
                activeforeground="#FFFFFF",
                highlightbackground=button_bg,
                highlightcolor="#FFFFFF"
            )
            
            # Configurar el menú desplegable
            self.instruction_menu["menu"].config(
                background="#444444",
                foreground="#FFFFFF",
                activebackground="#666666",
                activeforeground="#FFFFFF"
            )
        
        self.instruction_menu.pack(side=tk.LEFT, fill=tk.X)
        
        # Vincular evento de cambio
        self.instruction_var.trace("w", self._on_instruction_selected)
        
        self.clear_btn = ttk.Button(
            self.btn_frame, 
            text="Limpiar",
            command=self._handle_clear,
            style="Context.TButton",
            padding=button_padding
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
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
        self.context_text.tag_configure("instruction_header", font=("TkDefaultFont", 10, "bold"), foreground="purple")
        self.context_text.tag_configure("instruction_content", font=("TkDefaultFont", 9, "normal"))
        
        # Menú contextual para el área de contexto
        self.context_menu = tk.Menu(self.context_text, tearoff=0)
        self.context_menu.add_command(label="Eliminar selección", command=self._handle_remove_selected)
        
        # Vincular eventos
        self.context_text.bind("<Button-3>", self._show_context_menu)
    
    def _handle_stats(self):
        """Maneja el evento de mostrar estadísticas del contexto."""
        if self.on_stats:
            self.on_stats()
            
    def _handle_instructions(self):
        """Maneja el evento de gestionar instrucciones extra."""
        if self.on_instructions:
            self.on_instructions()
            
    def _on_instruction_selected(self, *args):
        """Maneja la selección de una instrucción en el desplegable."""
        if not self.instruction_manager:
            return
            
        # Obtener la instrucción seleccionada
        selected = self.instruction_var.get()
        
        # Si es "Sin instrucción", desactivar
        if selected == "Sin instrucción":
            self.instruction_manager.set_current_instruction(None)
        else:
            self.instruction_manager.set_current_instruction(selected)
    
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
        
        # Mostrar instrucción actual si existe
        if self.instruction_manager and self.instruction_manager.get_current_instruction():
            instruction_name = self.instruction_manager.get_current_instruction()
            instruction_content = self.instruction_manager.get_current_instruction_content()
            
            if instruction_content:
                # Mostrar encabezado para la instrucción
                header = f"### INSTRUCCIÓN EXTRA: {instruction_name} ###\n"
                self.context_text.insert(tk.END, header, "instruction_header")
                
                # Mostrar contenido
                self.context_text.insert(tk.END, instruction_content + "\n\n", "instruction_content")
        
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
        
    def set_instruction_manager(self, instruction_manager):
        """
        Establece el gestor de instrucciones y actualiza el desplegable.
        
        Args:
            instruction_manager: Gestor de instrucciones
        """
        self.instruction_manager = instruction_manager
        self._update_instruction_combobox()
        
    def _update_instruction_combobox(self):
        """Actualiza el desplegable con las instrucciones disponibles."""
        if not self.instruction_manager:
            return
        
        # Obtener todas las instrucciones
        instruction_names = self.instruction_manager.get_instruction_names()
        
        # Actualizar el menú desplegable
        menu = self.instruction_menu["menu"]
        menu.delete(0, tk.END)  # Limpiar menú actual
        
        # Añadir opción por defecto
        menu.add_command(label="Sin instrucción", 
                       command=lambda v="Sin instrucción": self.instruction_var.set(v))
        
        # Añadir instrucciones
        if instruction_names:
            instruction_names.sort()
            for name in instruction_names:
                menu.add_command(label=name, 
                               command=lambda v=name: self.instruction_var.set(v))
        
        # Seleccionar la instrucción actual
        current = self.instruction_manager.get_current_instruction()
        if current and current in instruction_names:
            self.instruction_var.set(current)
        else:
            self.instruction_var.set("Sin instrucción")
    
    def update_from_instruction_manager(self):
        """Método callback para el patrón Observer del InstructionManager."""
        self._update_instruction_combobox()
