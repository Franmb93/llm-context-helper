# Crear un nuevo archivo panel.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clases base para los paneles de la interfaz de usuario.
"""
import os
import tkinter as tk
from tkinter import ttk

class Panel:
    """Clase base para todos los paneles de la interfaz."""
    
    def __init__(self, parent):
        """
        Inicializa un panel genérico.
        
        Args:
            parent: Widget padre donde se creará este panel
        """
        self.parent = parent
        self.frame = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Método a sobrescribir en las clases derivadas."""
        pass
    
    def pack(self, **kwargs):
        """Empaqueta el frame del panel en su contenedor."""
        if self.frame:
            self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Coloca el frame del panel usando grid."""
        if self.frame:
            self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Coloca el frame del panel usando place."""
        if self.frame:
            self.frame.place(**kwargs)

class FileTreePanel(Panel):
    """Panel para mostrar y seleccionar archivos."""
    
    def __init__(self, parent, on_file_select, on_checkbox_click, on_add_selected_files=None):
        """
        Inicializa el panel de archivos.
        
        Args:
            parent: Widget padre
            on_file_select: Callback para cuando se selecciona un archivo
            on_checkbox_click: Callback para cuando se hace clic en una casilla
            on_add_selected_files: Callback para añadir múltiples archivos seleccionados
        """
        self.on_file_select = on_file_select
        self.on_checkbox_click = on_checkbox_click
        self.on_add_selected_files = on_add_selected_files
        self.show_hidden_files = False  # Agregar opción para archivos ocultos
        super().__init__(parent)
    
    def _create_widgets(self):
        """Crea los widgets del panel de archivos."""
        self.frame = ttk.Frame(self.parent)
        
        # Botón para seleccionar carpeta - Estilo más moderno
        self.folder_frame = ttk.Frame(self.frame, padding=(5, 5, 5, 5))
        self.folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Crear un estilo personalizado para el botón de selección de carpeta
        style = ttk.Style()
        style.configure("Folder.TButton", 
                         font=("Segoe UI", 9, "normal"))
        
        self.folder_btn = ttk.Button(self.folder_frame, text="Seleccionar carpeta", 
                                     command=self._on_select_folder,
                                     style="Folder.TButton")
        self.folder_btn.pack(side=tk.LEFT, padx=5)
        
        # Etiqueta con estilo más moderno
        self.current_folder_var = tk.StringVar(value="Ninguna carpeta seleccionada")
        self.folder_label = ttk.Label(self.folder_frame, textvariable=self.current_folder_var, 
                                    font=("Segoe UI", 9, "italic"))
        self.folder_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Frame para botones de acciones múltiples
        self.actions_frame = ttk.Frame(self.frame, padding=(5, 0, 5, 5))
        self.actions_frame.pack(fill=tk.X, padx=5, pady=0)
        
        # Estilo para botones de acción
        style.configure("Action.TButton", 
                         font=("Segoe UI", 9, "normal"))
        
        # Botón para añadir múltiples archivos seleccionados
        self.add_selected_btn = ttk.Button(
            self.actions_frame,
            text="Añadir archivos seleccionados",
            command=self._on_add_selected_files,
            style="Action.TButton"
        )
        self.add_selected_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Marco para el árbol de archivos con estilo moderno
        self.file_frame = ttk.Frame(self.frame, padding=(5, 5, 5, 5))
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para botones de acciones múltiples
        self.actions_frame = ttk.Frame(self.frame)
        self.actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón para añadir múltiples archivos seleccionados
        self.add_selected_btn = ttk.Button(
            self.actions_frame,
            text="Añadir archivos seleccionados al contexto",
            command=self._on_add_selected_files
        )
        self.add_selected_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Scrollbar para el Treeview
        self.file_tree_scroll = ttk.Scrollbar(self.file_frame)
        self.file_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para mostrar la estructura de archivos
        self.file_tree = ttk.Treeview(self.file_frame, yscrollcommand=self.file_tree_scroll.set, selectmode="extended")
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        self.file_tree_scroll.config(command=self.file_tree.yview)
        
        # Configurar columnas del Treeview
        self.file_tree["columns"] = ("select",)
        self.file_tree.column("#0", width=250, minwidth=150)
        self.file_tree.column("select", width=50, minwidth=50, stretch=tk.NO)
        
        self.file_tree.heading("#0", text="Archivo")
        self.file_tree.heading("select", text="Incluir")
        
        # Crear menú contextual para el árbol
        self.tree_menu = tk.Menu(self.file_tree, tearoff=0)
        self.tree_menu.add_command(
            label="Añadir al contexto",
            command=self._on_add_selected_files
        )
        self.tree_menu.add_command(
            label="Marcar como no incluidos",
            command=lambda: self._set_checkbox_state(False)
        )
        self.tree_menu.add_separator()
        self.tree_menu.add_command(
            label="Seleccionar todos",
            command=lambda: self._select_all_files(None)
        )
        
        # Vincular eventos
        self.file_tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.file_tree.bind("<ButtonRelease-1>", self._handle_checkbox_click)
        
        # Vincular clic derecho al menú contextual
        self.file_tree.bind("<Button-3>", self._show_tree_context_menu)
        
        # Vincular teclas de acceso rápido para selección múltiple
        self.file_tree.bind("<Control-a>", self._select_all_files)
    
    def _on_select_folder(self):
        """Notifica que se debe seleccionar una carpeta."""
        # Esta función solo reenvía el evento, la implementación real está en ContextSelector
        if hasattr(self.parent, "_open_folder"):
            self.parent._open_folder()
    
    def _on_tree_select(self, event):
        """Maneja la selección de un archivo."""
        if self.on_file_select:
            self.on_file_select(self.file_tree)
    
    def _handle_checkbox_click(self, event):
        """Maneja el clic en una casilla de verificación."""
        if self.on_checkbox_click:
            self.on_checkbox_click(event, self.file_tree)
    
    def _on_add_selected_files(self):
        """Llama al callback para añadir los archivos seleccionados al contexto."""
        if self.on_add_selected_files:
            selected_items = self.file_tree.selection()
            if selected_items:
                self.on_add_selected_files(selected_items)
    
    def _show_tree_context_menu(self, event):
        """Muestra el menú contextual para el árbol de archivos."""
        # Seleccionar el elemento bajo el cursor si no está seleccionado
        item = self.file_tree.identify_row(event.y)
        if item and item not in self.file_tree.selection():
            # Limpiar selección anterior si no se presiona Control
            if not (event.state & 4):  # 4 es el valor para Control presionado
                self.file_tree.selection_set(item)
        
        # Mostrar el menú contextual
        if self.file_tree.selection():
            self.tree_menu.tk_popup(event.x_root, event.y_root)
        
        return "break"  # Prevenir comportamiento por defecto
    
    def _select_all_files(self, event):
        """Selecciona todos los archivos visibles en el árbol."""
        for item in self.file_tree.get_children():
            self.file_tree.selection_add(item)
            # También seleccionar hijos recursivamente
            self._select_children(item)
        return "break"  # Prevenir la propagación del evento
    
    def _select_children(self, parent_item):
        """Selecciona recursivamente todos los hijos de un elemento."""
        for child in self.file_tree.get_children(parent_item):
            self.file_tree.selection_add(child)
            self._select_children(child)
    
    def _set_checkbox_state(self, checked):
        """
        Cambia el estado de las casillas de verificación para los elementos seleccionados.
        
        Args:
            checked (bool): True para marcar, False para desmarcar
        """
        for item_id in self.file_tree.selection():
            # Verificar si es un archivo (no directorio)
            item_tags = self.file_tree.item(item_id, "tags")
            if "file" in item_tags:
                # Actualizar el valor en el árbol
                new_state = "☑" if checked else "☐"
                self.file_tree.item(item_id, values=(new_state,))
                
                # Si hay callback para clic en checkbox, notificar el cambio
                if self.on_checkbox_click and self.on_add_selected_files:
                    # Crear un evento sintético para el clic en checkbox
                    file_path = self.parent._get_full_path(item_id, self.file_tree)
                    if file_path:
                        if checked:
                            self.on_add_selected_files([item_id])
                        else:
                            # Eliminar del contexto (esto requiere acceso al SelectionManager)
                            if hasattr(self.parent, "selection_manager"):
                                self.parent.selection_manager.remove_file(file_path)
    
    def set_current_folder(self, folder_path):
        """Actualiza la carpeta mostrada."""
        self.current_folder_var.set(folder_path)
    
    def setup_line_numbers(self, line_numbers_widget):
        """
        Configura el widget de números de línea y la sincronización.
        
        Args:
            line_numbers_widget: Widget Text para los números de línea
        """
        self.line_numbers = line_numbers_widget
        self.show_line_numbers = True
        
        # Configurar eventos para mantener sincronización
        self.content_text.bind("<MouseWheel>", self._on_mousewheel)
        self.content_text.bind("<Button-4>", self._on_mousewheel)
        self.content_text.bind("<Button-5>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        """
        Maneja eventos de rueda del ratón para sincronizar el desplazamiento.
        """
        if hasattr(self, 'line_numbers') and self.show_line_numbers:
            # Sincronizar la posición de desplazamiento
            self.line_numbers.yview_moveto(self.content_text.yview()[0])
        return "break"  # No propagar el evento
    
    def clear_tree(self):
        """Limpia todos los elementos del árbol."""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
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
    
    def _set_checkbox_state(self, checked):
        """
        Cambia el estado de las casillas de verificación para los elementos seleccionados.
        
        Args:
            checked (bool): True para marcar, False para desmarcar
        """
        for item_id in self.file_tree.selection():
            # Verificar si es un archivo (no directorio)
            item_tags = self.file_tree.item(item_id, "tags")
            if "file" in item_tags:
                # Actualizar el valor en el árbol
                new_state = "☑" if checked else "☐"
                self.file_tree.item(item_id, values=(new_state,))
                
                # Si hay callback para clic en checkbox, notificar el cambio
                if self.on_checkbox_click and self.on_add_selected_files:
                    # Crear un evento sintético para el clic en checkbox
                    file_path = self.parent._get_full_path(item_id, self.file_tree)
                    if file_path:
                        if checked:
                            self.on_add_selected_files([item_id])
                        else:
                            # Eliminar del contexto (esto requiere acceso al SelectionManager)
                            if hasattr(self.parent, "selection_manager"):
                                self.parent.selection_manager.remove_file(file_path)
    
    def _show_tree_context_menu(self, event):
        """Muestra el menú contextual para el árbol de archivos."""
        # Seleccionar el elemento bajo el cursor si no está seleccionado
        item = self.file_tree.identify_row(event.y)
        if item and item not in self.file_tree.selection():
            # Limpiar selección anterior si no se presiona Control
            if not (event.state & 4):  # 4 es el valor para Control presionado
                self.file_tree.selection_set(item)
        
        # Mostrar el menú contextual
        if self.file_tree.selection():
            self.tree_menu.tk_popup(event.x_root, event.y_root)
        
        return "break"
    
    def _create_widgets(self):
        """Crea los widgets del panel de contenido."""
        self.frame = ttk.LabelFrame(self.parent, text="Contenido del archivo", padding=(8, 5, 8, 8))
        self.frame = ttk.LabelFrame(self.parent, text="Contenido del archivo")
        
        # Determinar el tema actual para configurar los colores adecuados
        try:
            app_settings_file = os.path.join(os.path.dirname(__file__), "..", "config", "app_settings.json")
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
    
    # Modificar FileContentPanel.load_file para que sea más directo
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
        
# Agregar a panel.py
class ContextPanel(Panel):
    """Panel para mostrar y gestionar el contexto seleccionado."""
    
    def __init__(self, parent, on_copy, on_save, on_clear, on_context_menu, on_stats=None):
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
        self.frame = ttk.LabelFrame(self.parent, text="Contexto seleccionado")
        
        # Botones para el contexto
        self.btn_frame = ttk.Frame(self.frame)
        self.btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.copy_btn = ttk.Button(
            self.btn_frame, 
            text="Copiar al portapapeles", 
            command=self._handle_copy
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(
            self.btn_frame, 
            text="Guardar contexto", 
            command=self._handle_save
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_btn = ttk.Button(
            self.btn_frame,
            text="Estadísticas",
            command=self._handle_stats
        )
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            self.btn_frame, 
            text="Limpiar contexto", 
            command=self._handle_clear
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Crear widget Text para el contexto con scrollbars
        self.context_scrolly = ttk.Scrollbar(self.frame)
        self.context_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.context_scrollx = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.context_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Determinar el tema actual para configurar los colores adecuados
        try:
            app_settings_file = os.path.join(os.path.dirname(__file__), "..", "config", "app_settings.json")
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

        pass
    
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
        
        self.context_text.config(state=tk.NORMAL)
        
    def set_remove_handler(self, handler):
        """
        Establece el controlador para eliminar selecciones.
        
        Args:
            handler: Función a llamar cuando se elimina una selección
        """
        self.context_menu.entryconfig(
            self.context_menu.index("Eliminar selección"),
            command=handler
        )