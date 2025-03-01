# Modificar context_selector.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase principal para la aplicación Selector de Contexto para LLMs.
Implementa la interfaz gráfica principal utilizando Tkinter.
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils import create_custom_scroll_event
from file_manager import FileManager
from syntax_highlighter import SyntaxHighlighter
from selection_manager import SelectionManager
from panel import FileTreePanel, FileContentPanel, ContextPanel
from utils import copy_to_clipboard, save_to_file

class ContextSelector(tk.Tk):
    """Clase principal que implementa la interfaz gráfica del selector de contexto."""
    
    def __init__(self):
        """Inicializa la aplicación y configura la interfaz gráfica."""
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Selector de Contexto para LLMs")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Variables de estado
        self.current_folder = None
        self.current_file = None
        
        # Inicializar componentes
        self.file_manager = FileManager()
        self.syntax_highlighter = SyntaxHighlighter()
        self.selection_manager = SelectionManager()
        
        # Registrar como observador
        self.selection_manager.add_observer(self)
        
        # Cargar configuración guardada primero, antes de crear la interfaz
        self._load_settings()
        
        # Establecer un icono y configurar la ventana para que sea más moderna
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
        icon_path = os.path.join(assets_dir, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(default=icon_path)
        
        # Establecer padding global
        self.main_padding = 10
        
        # Crear íconos para el árbol de archivos
        self._create_dummy_icons()
        
        # Crear la interfaz
        self._create_menu()
        self._create_main_layout()
        
        self.context_panel.set_remove_handler(self._remove_selected_text)
        create_custom_scroll_event(self)
        
        # Aplicar estilo moderno y tema configurado
        self._apply_settings(self._get_current_settings())
        
        # Cargar la carpeta anterior si existe
        if self.current_folder:
            self.file_tree_panel.set_current_folder(self.current_folder)
            self._load_files()

    def _get_current_settings(self):
        """Obtiene las configuraciones actuales o usa valores predeterminados."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            app_settings_file = os.path.join(config_dir, "app_settings.json")
            
            if os.path.exists(app_settings_file):
                with open(app_settings_file, 'r') as f:
                    return json.load(f)
            
            # Si no hay configuración, devolver valores predeterminados
            return {
                'general': {
                    'theme': 'light',
                    'font_size': 10,
                    'word_wrap': False,
                    'show_line_numbers': True
                }
            }
        except Exception as e:
            print(f"Error al obtener configuración actual: {str(e)}")
            # En caso de error, devolver configuración predeterminada
            return {'general': {'theme': 'light'}}

    def _apply_modern_style(self):
            """Aplica un estilo moderno a la aplicación."""
            style = ttk.Style()
            
            # Usar 'clam' como tema base ya que es uno de los más personalizables
            style.theme_use("clam")
            
            # Configurar colores base para un tema claro moderno
            bg_color = "#F8F8F8"           # Fondo principal
            fg_color = "#333333"           # Texto
            select_bg = "#0078D7"          # Color de selección
            select_fg = "#FFFFFF"          # Texto sobre selección
            frame_bg = "#F0F0F0"           # Fondo de marcos
            border_color = "#DDDDDD"       # Color de bordes
            
            # Configuración general
            style.configure(".", 
                        background=bg_color, 
                        foreground=fg_color, 
                        bordercolor=border_color,
                        focuscolor=select_bg)
            
            # Frames con bordes suaves
            style.configure("TFrame", 
                        background=frame_bg, 
                        borderwidth=0)
            
            # LabelFrames con bordes redondeados
            style.configure("TLabelFrame", 
                        background=frame_bg, 
                        borderwidth=1, 
                        relief="groove")
            
            style.configure("TLabelFrame.Label", 
                        background=frame_bg, 
                        foreground=fg_color,
                        font=("Segoe UI", 9, "normal"))
            
            # Botones más modernos
            style.configure("TButton", 
                        background="#FFFFFF", 
                        foreground=fg_color, 
                        relief="flat",
                        borderwidth=1,
                        padding=(8, 4),
                        font=("Segoe UI", 9, "normal"))
            
            # Efecto hover para botones
            style.map("TButton",
                    background=[("active", select_bg), ("pressed", select_bg)],
                    foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")],
                    relief=[("active", "flat"), ("pressed", "flat")])
            
            # Configurar el Panedwindow para que sea más moderno
            style.configure("TPanedwindow", 
                        background=bg_color)
            
            # Configurar separadores de paneles
            style.configure("Sash", 
                        background="#CCCCCC",
                        sashthickness=4)
            
            # Aplicar a la ventana principal
            self.configure(background=bg_color)
            
            
    def _create_menu(self):
        """Crea la barra de menú principal."""
        self.menu_bar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir carpeta", command=self._open_folder, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Guardar contexto", command=self._save_context, accelerator="Ctrl+S")
        file_menu.add_command(label="Guardar selecciones", command=self._save_selections, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Cargar selecciones", command=self._load_selections, accelerator="Ctrl+Shift+O")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Edición
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Copiar selección", command=self._copy_selection, accelerator="Ctrl+C")
        edit_menu.add_command(label="Añadir selección al contexto", command=self._add_selection, accelerator="Alt+A")
        edit_menu.add_separator()
        
        # Submenú para selecciones múltiples
        multi_select_menu = tk.Menu(edit_menu, tearoff=0)
        multi_select_menu.add_command(
            label="Añadir archivos seleccionados", 
            command=lambda: self._add_selected_files_to_context(self.file_tree_panel.file_tree.selection()),
            accelerator="Alt+M"
        )
        multi_select_menu.add_command(
            label="Seleccionar todos los archivos", 
            command=lambda: self.file_tree_panel._select_all_files(None),
            accelerator="Ctrl+A"
        )
        multi_select_menu.add_separator()
        multi_select_menu.add_command(
            label="Marcar seleccionados como no incluidos", 
            command=lambda: self.file_tree_panel._set_checkbox_state(False)
        )
        edit_menu.add_cascade(label="Selección múltiple", menu=multi_select_menu)
        
        edit_menu.add_separator()
        edit_menu.add_command(label="Buscar en selecciones", command=self._search_selections, accelerator="Ctrl+F")
        edit_menu.add_separator()
        edit_menu.add_command(label="Estadísticas del contexto", command=self._show_context_stats, accelerator="Ctrl+T")
        edit_menu.add_command(label="Limpiar contexto", command=self._clear_context, accelerator="Ctrl+L")
        self.menu_bar.add_cascade(label="Edición", menu=edit_menu)
        
        # Menú Preferencias
        pref_menu = tk.Menu(self.menu_bar, tearoff=0)
        pref_menu.add_command(label="Configuración", command=self._open_settings)
        self.menu_bar.add_cascade(label="Preferencias", menu=pref_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self._show_about)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.config(menu=self.menu_bar)
        
        # Atajos de teclado
        self.bind("<Control-o>", lambda event: self._open_folder())
        self.bind("<Control-s>", lambda event: self._save_context())
        self.bind("<Control-l>", lambda event: self._clear_context())
        self.bind("<Alt-a>", lambda event: self._add_selection())
        self.bind("<Control-f>", lambda event: self._search_selections())
        self.bind("<Control-Shift-s>", lambda event: self._save_selections())
        self.bind("<Control-Shift-o>", lambda event: self._load_selections())
        
        # Atajos para selección múltiple
        self.bind("<Alt-m>", lambda event: self._add_selected_files_to_context(self.file_tree_panel.file_tree.selection()))
        self.bind("<Control-t>", lambda event: self._show_context_stats())
    
    def _create_main_layout(self):
        """Crea el diseño principal de la interfaz con paneles."""
        # Contenedor principal con paneles ajustables y padding
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=self.main_padding, pady=self.main_padding)
        
        # Panel izquierdo (lista de archivos)
        self.file_tree_panel = FileTreePanel(
            self,
            on_file_select=self._on_file_select,
            on_checkbox_click=self._on_checkbox_click,
            on_add_selected_files=self._add_selected_files_to_context
        )
        self.main_paned.add(self.file_tree_panel.frame, weight=1)
        
        # Panel derecho (contenido + contexto)
        self.right_paned = ttk.PanedWindow(self.main_paned, orient=tk.VERTICAL)
        self.main_paned.add(self.right_paned, weight=3)
        
        # Panel superior (visualización de archivos)
        self.file_content_panel = FileContentPanel(
            self.right_paned,
            syntax_highlighter=self.syntax_highlighter,
            on_add_selection=self._add_selection_from_panel,
            on_context_menu=self._show_file_context_menu
        )
        self.right_paned.add(self.file_content_panel.frame, weight=2)
        
        # Panel inferior (contexto recopilado)
        self.context_panel = ContextPanel(
            self.right_paned,
            on_copy=self._copy_context,
            on_save=self._save_context,
            on_clear=self._clear_context,
            on_context_menu=self._show_context_menu,
            on_stats=self._show_context_stats
        )
        self.right_paned.add(self.context_panel.frame, weight=1)
    
    def _create_dummy_icons(self):
        """Crea íconos temporales para el árbol de archivos."""
        # Este método crea íconos básicos para desarrollo
        # En una aplicación completa deberías usar archivos de imagen reales
        
        # Diccionario para almacenar los íconos
        self.tree_icons = {}
        
        # Crear una imagen base de 16x16 píxeles
        base_img = tk.PhotoImage(width=16, height=16)
        
        # Colores para los diferentes tipos
        colors = {
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
        for icon_name, color in colors.items():
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
            
            self.tree_icons[icon_name] = icon
    
    def update_from_selection_manager(self):
        """Método callback para el patrón Observer."""
        try:
            # Actualizar la visualización del contexto
            self._update_context_display()
            
            # Actualizar los resaltados visuales si el archivo actual está abierto
            if self.current_file:
                self.file_content_panel.clear_highlights()
                ranges = self.selection_manager.get_selection_ranges(self.current_file)
                if ranges:
                    self.file_content_panel.apply_highlights(ranges)
        except Exception as e:
            print(f"Error en update_from_selection_manager: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _open_folder(self):
        """Abre un diálogo para seleccionar una carpeta y la carga en el árbol."""
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder_path:
            self.current_folder = folder_path
            self.file_tree_panel.set_current_folder(folder_path)
            self._load_files()
            self._save_settings()
    
    # En el método _load_files
    def _load_files(self):
        """Carga los archivos de la carpeta seleccionada en el árbol."""
        # Limpiar el árbol actual
        self.file_tree_panel.clear_tree()
        
        if not self.current_folder:
            return
        
        # Asegurarnos de que la ruta esté normalizada
        self.current_folder = os.path.normpath(self.current_folder)
        
        # Obtener la lista de archivos y carpetas
        files = self.file_manager.scan_directory(self.current_folder)
        
        # Añadir cada archivo/carpeta al árbol
        for file_info in files:
            self._add_file_to_tree(file_info, "")
    
    def _add_file_to_tree(self, file_info, parent):
        """Añade un archivo o carpeta al árbol de archivos con ícono."""
        icon = "file"  
        
        if file_info["type"] == "directory":
            icon = "directory"
        elif "language" in file_info:
            lang = file_info["language"].lower()
            if lang in self.tree_icons:
                icon = lang
            elif lang == "python":
                icon = "python"
            elif lang in ["javascript", "js"]:
                icon = "javascript"
            elif lang == "html":
                icon = "html"
            elif lang == "css":
                icon = "css"
            elif lang in ["markdown", "md"]:
                icon = "markdown"
            elif lang == "json":
                icon = "json"
            elif lang == "xml":
                icon = "xml"
            elif lang in ["text", "txt"]:
                icon = "text"
        
        # Set checkbox value - only for files, not directories
        checkbox_value = "☐" if file_info["type"] == "file" else ""
        
        item_id = self.file_tree_panel.file_tree.insert(
            parent, 
            "end", 
            text=file_info["name"],
            values=(checkbox_value,),
            tags=(file_info["type"],),
            image=self.tree_icons.get(icon, self.tree_icons["file"])
        )
        
        if file_info["type"] == "directory" and "children" in file_info:
            for child in file_info["children"]:
                self._add_file_to_tree(child, item_id)
        
        return item_id
    
    def _on_file_select(self, tree):
        """Maneja el evento de selección de un archivo en el árbol."""
        selected_item = tree.selection()
        if not selected_item:
            return
        
        item_id = selected_item[0]
        item_tags = tree.item(item_id, "tags")
        
        # Si es un directorio, expandir/colapsar
        if "directory" in item_tags:
            if tree.item(item_id, "open"):
                tree.item(item_id, open=False)
            else:
                tree.item(item_id, open=True)
            return
        
        # Si es un archivo, cargar su contenido
        file_path = self._get_full_path(item_id, tree)
        if file_path and os.path.isfile(file_path):
            self._load_file_content(file_path)
    
    def _on_checkbox_click(self, event, tree):
        """Maneja los clics en la columna de casillas de verificación."""
        # Obtener la región donde se hizo clic
        region = tree.identify_region(event.x, event.y)
        
        # Verificar si se hizo clic en una celda
        if region == "cell":
            # Obtener la columna donde se hizo clic
            column = tree.identify_column(event.x)
            
            # Verificar si es la columna de casillas de verificación
            if column == "#1":
                item_id = tree.identify_row(event.y)
                if item_id:
                    # Obtener las etiquetas del elemento
                    item_tags = tree.item(item_id, "tags")
                    
                    # Solo procesar si es un archivo
                    if "file" in item_tags:
                        # Obtener el valor actual de la casilla
                        current_values = tree.item(item_id, "values")
                        current_state = current_values[0] if current_values else "☐"
                        
                        # Cambiar el estado
                        new_state = "☑" if current_state == "☐" else "☐"
                        
                        # Actualizar el valor en el árbol
                        tree.item(item_id, values=(new_state,))
                        
                        # Obtener la ruta completa del archivo
                        file_path = self._get_full_path(item_id, tree)
                        
                        # Actualizar según el nuevo estado
                        if new_state == "☑":
                            self._add_complete_file_to_context(file_path)
                        else:
                            self.selection_manager.remove_file(file_path)
    
    # En _get_full_path
    def _get_full_path(self, item_id, tree):
        """Obtiene la ruta completa de un elemento del árbol."""
        print(f"Obteniendo ruta para item_id: {item_id}")
        path_parts = []
        
        # Recorrer el árbol hacia arriba para construir la ruta
        current_item = item_id
        while current_item:
            item_text = tree.item(current_item, "text")
            print(f"  Componente de ruta: {item_text}")
            path_parts.insert(0, item_text)
            current_item = tree.parent(current_item)
        
        print(f"  Componentes completos: {path_parts}")
        print(f"  Carpeta base: {self.current_folder}")
        
        # Construir la ruta completa
        if self.current_folder:
            full_path = os.path.join(self.current_folder, *path_parts)
            print(f"  Ruta completa: {full_path}")
            print(f"  ¿Existe?: {os.path.exists(full_path)}")
            return full_path
        return None
    
    def _load_file_content(self, file_path):
        """Carga el contenido de un archivo en el panel de contenido."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            self.current_file = file_path
            
            # Actualizar el contenido en el panel
            self.file_content_panel.content_text.config(state=tk.NORMAL)
            self.file_content_panel.content_text.delete(1.0, tk.END)
            self.file_content_panel.content_text.insert(tk.END, content)
            
            # Aplicar resaltado de sintaxis según extensión
            file_ext = os.path.splitext(file_path)[1].lower()
            self.syntax_highlighter.highlight(self.file_content_panel.content_text, file_ext)
            
            # Aplicar resaltado a las selecciones previas (si existen)
            ranges = self.selection_manager.get_selection_ranges(file_path)
            if ranges:
                self.file_content_panel.apply_highlights(ranges)
            
            self.file_content_panel.content_text.config(state=tk.DISABLED)
            
            # Actualizar título del frame
            self.file_content_panel.frame.config(text=f"Contenido: {os.path.basename(file_path)}")
            
            # Actualizar números de línea
            if hasattr(self.file_content_panel, 'show_line_numbers') and self.file_content_panel.show_line_numbers:
                self._update_line_numbers()
                
                # Asegurar que el desplazamiento comienza desde el principio
                self.file_content_panel.content_text.yview_moveto(0.0)
                if hasattr(self.file_content_panel, 'line_numbers'):
                    self.file_content_panel.line_numbers.yview_moveto(0.0)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {file_path}\n\nDetalles: {str(e)}")
            
    def _add_selection_from_panel(self, text_widget):
        """Añade la selección actual al contexto desde el panel de contenido."""
        if not self.current_file:
            return
        
        # Obtener la selección actual
        try:
            selection = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            # Guardar también las posiciones de la selección
            sel_start = text_widget.index(tk.SEL_FIRST)
            sel_end = text_widget.index(tk.SEL_LAST)
        except tk.TclError:
            messagebox.showinfo("Sin selección", "No hay texto seleccionado")
            return
        
        if not selection:
            return
        
        # Usar el SelectionManager para añadir la selección
        success = self.selection_manager.add_selection(
            self.current_file, 
            selection, 
            (sel_start, sel_end)
        )
        
        if not success:
            if self.selection_manager.is_whole_file_in_context(self.current_file):
                messagebox.showinfo("Archivo ya incluido", 
                                "El archivo completo ya está incluido en el contexto. "
                                "La selección ya forma parte del contexto.")
            else:
                messagebox.showinfo("Selección duplicada", 
                                "Esta selección ya ha sido añadida al contexto.")

    def _add_selection(self):
        """Añade la selección actual al contexto (método para menú/atajo)."""
        self._add_selection_from_panel(self.file_content_panel.content_text)

    def _show_file_context_menu(self, event, text_widget, menu):
        """Muestra el menú contextual en el área de contenido de archivo."""
        try:
            text_widget.selection_get()
            menu.tk_popup(event.x_root, event.y_root)
        except:
            pass
        finally:
            menu.grab_release()

    def _add_complete_file_to_context(self, file_path):
        """Añade el contenido completo de un archivo al contexto."""
        try:
            # Verificar si el archivo existe y es legible
            if not os.path.isfile(file_path):
                return
            
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Usar el SelectionManager para añadir el archivo completo
            self.selection_manager.add_whole_file(file_path, content)
            
        except Exception as e:
            messagebox.showerror("Error al cargar archivo", f"No se pudo cargar el archivo: {str(e)}")

    def _update_context_display(self):
        """Actualiza la visualización del contexto seleccionado."""
        # Obtener todas las selecciones del SelectionManager
        selections = self.selection_manager.get_all_selections()
        
        # Actualizar el panel de contexto
        self.context_panel.update_context(selections)

    def _show_context_menu(self, event, text_widget, menu):
        """Muestra el menú contextual en el área de contexto."""
        try:
            # Marcar la posición del clic
            text_widget.mark_set("insert", f"@{event.x},{event.y}")
            
            # Determinar si el clic está dentro de alguna selección
            current_pos = text_widget.index("insert")
            pos_line, pos_col = map(int, current_pos.split('.'))
            
            # Verificar si estamos dentro de alguna de las selecciones
            selection_found = False
            
            for file_path, markers in self.context_panel.context_selection_markers.items():
                for marker in markers:
                    idx, start_pos, end_pos, is_whole_file = marker
                    
                    start_line, start_col = map(int, start_pos.split('.'))
                    end_line, end_col = map(int, end_pos.split('.'))
                    
                    # Si la posición actual está dentro de esta selección
                    if (pos_line > start_line or (pos_line == start_line and pos_col >= start_col)) and \
                    (pos_line < end_line or (pos_line == end_line and pos_col <= end_col)):
                        # Resaltar visualmente la selección en el área de contexto
                        text_widget.tag_remove("selection_highlight", "1.0", tk.END)
                        text_widget.tag_add("selection_highlight", start_pos, end_pos)
                        
                        # Guardar la referencia a la selección para poder eliminarla
                        self.current_context_selection = (file_path, idx, is_whole_file)
                        
                        # Mostrar el menú contextual
                        menu.tk_popup(event.x_root, event.y_root)
                        selection_found = True
                        break
                
                if selection_found:
                    break
        except Exception as e:
            print(f"Error en el menú contextual: {str(e)}")
        finally:
            menu.grab_release()

    def _copy_selection(self):
        """Copia la selección actual al portapapeles."""
        self.file_content_panel._copy_selection()

    def _copy_context(self):
        """Copia todo el contexto al portapapeles."""
        context = self.selection_manager.get_formatted_context()
        if context:
            copy_to_clipboard(self, context)
            messagebox.showinfo("Contexto copiado", "El contexto ha sido copiado al portapapeles")
        else:
            messagebox.showinfo("Sin contexto", "No hay contexto para copiar")

    def _save_context(self):
        """Guarda el contexto en un archivo."""
        context = self.selection_manager.get_formatted_context()
        if not context:
            messagebox.showinfo("Sin contexto", "No hay contexto para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar contexto"
        )
        
        if file_path:
            save_to_file(context, file_path)
            messagebox.showinfo("Contexto guardado", f"El contexto ha sido guardado en:\n{file_path}")

    def _clear_context(self):
        """Limpia todo el contexto seleccionado."""
        if messagebox.askyesno("Limpiar contexto", "¿Está seguro de que desea limpiar todo el contexto?"):
            self.selection_manager.clear_all()

    def _save_selections(self):
        """Guarda las selecciones en un archivo."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Guardar selecciones"
        )
        
        if file_path:
            if self.selection_manager.save_selections_to_file(file_path):
                messagebox.showinfo("Selecciones guardadas", f"Las selecciones han sido guardadas en:\n{file_path}")
            else:
                messagebox.showerror("Error", "No se pudieron guardar las selecciones")

    def _load_selections(self):
        """Carga selecciones desde un archivo."""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Cargar selecciones"
        )
        
        if file_path:
            if self.selection_manager.load_selections_from_file(file_path):
                messagebox.showinfo("Selecciones cargadas", "Las selecciones han sido cargadas correctamente")
            else:
                messagebox.showerror("Error", "No se pudieron cargar las selecciones")

    def _update_checkbox_state(self, file_path, checked):
        """Actualiza el estado de la casilla de verificación para un archivo."""
        # Encontrar el ítem en el árbol que corresponde a esta ruta
        file_name = os.path.basename(file_path)
        
        # Buscar este archivo en el árbol
        for item_id in self._find_file_item_by_name(file_name):
            full_path = self._get_full_path(item_id, self.file_tree_panel.file_tree)
            if full_path == file_path:
                # Actualizar el valor en el árbol
                new_state = "☑" if checked else "☐"
                self.file_tree_panel.file_tree.item(item_id, values=(new_state,))
                break

    def _find_file_item_by_name(self, file_name):
        """Encuentra todos los items del árbol que coinciden con un nombre de archivo."""
        result = []
        
        def _find_in_children(parent):
            for item_id in self.file_tree_panel.file_tree.get_children(parent):
                if self.file_tree_panel.file_tree.item(item_id, "text") == file_name:
                    result.append(item_id)
                _find_in_children(item_id)
        
        _find_in_children('')  # Empezar desde la raíz
        return result

    def _search_selections(self):
        """Abre un diálogo para buscar en las selecciones."""
        search_text = tk.simpledialog.askstring("Buscar", "Texto a buscar en las selecciones:")
        if not search_text:
            return
        
        results = self.selection_manager.search_in_selections(search_text)
        
        if not results:
            messagebox.showinfo("Búsqueda", f"No se encontró '{search_text}' en ninguna selección.")
            return
        
        # Crear una ventana para mostrar resultados
        search_window = tk.Toplevel(self)
        search_window.title(f"Resultados de búsqueda: '{search_text}'")
        search_window.geometry("600x400")
        
        # Crear un Treeview para mostrar los resultados
        tree_frame = ttk.Frame(search_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=("file", "selection", "position"))
        tree.heading("#0", text="Archivo")
        tree.heading("file", text="Archivo")
        tree.heading("selection", text="Selección")
        tree.heading("position", text="Posición")
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("file", width=150)
        tree.column("selection", width=300)
        tree.column("position", width=100)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Llenar el árbol con resultados
        for file_path, file_results in results.items():
            file_name = os.path.basename(file_path)
            
            for i, (selection_idx, selection, start, end) in enumerate(file_results):
                # Truncar la selección si es muy larga
                preview = selection
                if len(preview) > 50:
                    preview = preview[:47] + "..."
                
                tree.insert("", "end", text="", values=(file_name, preview, f"{start}-{end}"))

    def _setup_line_numbers(self):
        """Set up line numbers for the file content panel."""
        if not hasattr(self.file_content_panel, 'line_numbers'):
            # Get current theme colors
            bg_color = "#383838" if self._get_current_theme() == "dark" else "#f0f0f0"
            fg_color = "#FFFFFF" if self._get_current_theme() == "dark" else "#606060"
            
            # Create a Text widget for line numbers with proper colors
            self.file_content_panel.line_numbers = tk.Text(
                self.file_content_panel.frame,
                width=4,
                padx=4,
                highlightthickness=0,
                takefocus=0,
                bd=0,
                background=bg_color,
                foreground=fg_color,
                font=self.file_content_panel.content_text.cget('font')
            )
            
            # Insert line numbers to the left of the content text (must adjust the layout)
            self.file_content_panel.content_text.pack_forget()
            self.file_content_panel.content_scrolly.pack_forget()
            self.file_content_panel.content_scrollx.pack_forget()
            
            # Create a frame to hold the line numbers and text
            if not hasattr(self.file_content_panel, 'text_frame'):
                self.file_content_panel.text_frame = ttk.Frame(self.file_content_panel.frame)
                self.file_content_panel.text_frame.pack(fill=tk.BOTH, expand=True)
            
            # Place all components
            self.file_content_panel.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
            self.file_content_panel.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.file_content_panel.content_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            self.file_content_panel.content_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Make line numbers read-only
            self.file_content_panel.line_numbers.config(state=tk.DISABLED)
            
            # Sincronizar los ScrollBars para ambos Text widgets
            # Guardar el comando original de la barra de desplazamiento
            original_command = self.file_content_panel.content_scrolly.cget('command')
            
            # Definir una nueva función que actualice ambos widgets
            def on_content_scroll(*args):
                # Desactivar temporalmente el tracking de cambios para evitar recursión
                self.file_content_panel._scroll_updating = True
                
                # Aplicar desplazamiento al widget de contenido
                self.file_content_panel.content_text.yview(*args)
                
                # Sincronizar el widget de números de línea exactamente a la misma posición
                self.file_content_panel.line_numbers.yview_moveto(
                    self.file_content_panel.content_text.yview()[0]
                )
                
                # Reactivar el tracking de cambios
                self.file_content_panel._scroll_updating = False
            
            # Aplicar la nueva función al ScrollBar
            self.file_content_panel.content_scrolly.config(command=on_content_scroll)
            
            # Necesitamos capturar también cuando el usuario mueve directamente el texto
            # para sincronizar números de línea
            def on_text_scroll_change(*args):
                if hasattr(self.file_content_panel, '_scroll_updating') and self.file_content_panel._scroll_updating:
                    return
                
                # Sincronizar el widget de números de línea
                self.file_content_panel.line_numbers.yview_moveto(
                    self.file_content_panel.content_text.yview()[0]
                )
            
            # Detectar cambios de desplazamiento en el texto
            self.file_content_panel.content_text.config(yscrollcommand=lambda *args: [
                self.file_content_panel.content_scrolly.set(*args),
                on_text_scroll_change()
            ])
            
            # También necesitamos manejar el desplazamiento directo del widget de números de línea
            def on_linenumbers_scroll(*args):
                if hasattr(self.file_content_panel, '_scroll_updating') and self.file_content_panel._scroll_updating:
                    return
                    
                # Desactivar temporalmente el tracking
                self.file_content_panel._scroll_updating = True
                
                # Sincronizar el widget de contenido con los números de línea
                self.file_content_panel.content_text.yview_moveto(
                    self.file_content_panel.line_numbers.yview()[0]
                )
                
                # Reactivar el tracking
                self.file_content_panel._scroll_updating = False
            
            # Capturar eventos de desplazamiento de la rueda del mouse
            self.file_content_panel.content_text.bind("<MouseWheel>", self._on_mousewheel)
            self.file_content_panel.line_numbers.bind("<MouseWheel>", self._on_mousewheel)
            
            # Para Linux también necesitamos capturar estos eventos
            self.file_content_panel.content_text.bind("<Button-4>", self._on_mousewheel)
            self.file_content_panel.content_text.bind("<Button-5>", self._on_mousewheel)
            self.file_content_panel.line_numbers.bind("<Button-4>", self._on_mousewheel)
            self.file_content_panel.line_numbers.bind("<Button-5>", self._on_mousewheel)
            
            # Flag para seguimiento
            self.file_content_panel.show_line_numbers = True
            self.file_content_panel._scroll_updating = False
            
            # Generar números de línea iniciales
            self._update_line_numbers()

    def _on_mousewheel(self, event):
        """Maneja eventos de rueda del ratón para sincronizar desplazamiento."""
        if not hasattr(self.file_content_panel, 'line_numbers'):
            return
        
        # Determinar la dirección del desplazamiento y la cantidad
        if event.num == 4 or event.delta > 0:  # Scroll up
            direction = -1
        elif event.num == 5 or event.delta < 0:  # Scroll down
            direction = 1
        else:
            return
        
        # Aplicar desplazamiento a ambos widgets
        self.file_content_panel._scroll_updating = True
        
        # Usar unidades más pequeñas para un desplazamiento más suave
        self.file_content_panel.content_text.yview_scroll(direction, "units")
        
        # Sincronizar la posición exactamente
        self.file_content_panel.line_numbers.yview_moveto(
            self.file_content_panel.content_text.yview()[0]
        )
        
        self.file_content_panel._scroll_updating = False
        
        # Prevenir manejo adicional
        return "break"

    # Modificar el método _update_line_numbers para mejor rendimiento
    def _update_line_numbers(self, event=None):
        """Update the line numbers displayed in the file content panel."""
        if not hasattr(self.file_content_panel, 'line_numbers') or not self.file_content_panel.show_line_numbers:
            return
        
        # Guardar la posición actual de desplazamiento
        current_pos = self.file_content_panel.content_text.yview()[0]
        
        # Make line numbers widget editable temporarily
        self.file_content_panel.line_numbers.config(state=tk.NORMAL)
        
        # Clear existing line numbers
        self.file_content_panel.line_numbers.delete('1.0', tk.END)
        
        # Count total lines in the file
        last_line = self.file_content_panel.content_text.index('end-1c')
        total_lines = int(last_line.split('.')[0])
        
        # Generate line numbers text
        line_numbers_text = '\n'.join(str(i) for i in range(1, total_lines + 1))
        
        # Insert line numbers
        self.file_content_panel.line_numbers.insert('1.0', line_numbers_text)
        
        # Make line numbers widget read-only again
        self.file_content_panel.line_numbers.config(state=tk.DISABLED)
        
        # Restaurar posición de desplazamiento exactamente
        self.file_content_panel._scroll_updating = True
        self.file_content_panel.line_numbers.yview_moveto(current_pos)
        self.file_content_panel._scroll_updating = False

    def _get_current_theme(self):
        """Get the current theme name from settings."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            app_settings_file = os.path.join(config_dir, "app_settings.json")
            if os.path.exists(app_settings_file):
                with open(app_settings_file, 'r') as f:
                    app_settings = json.load(f)
                
                if 'general' in app_settings and 'theme' in app_settings['general']:
                    theme = app_settings['general']['theme']
                    # Si el tema es 'system', determinar basado en configuración del sistema
                    if theme == 'system':
                        # Simplemente devolver 'light' como predeterminado para 'system'
                        # En una implementación completa, verificaríamos el tema del sistema
                        return 'light'
                    return theme
        except Exception as e:
            print(f"Error obteniendo tema actual: {str(e)}")
        
        return "light"  # Tema predeterminado

    def _open_settings(self):
        """Opens the settings dialog to configure application preferences."""
        # Create a top-level window for settings
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("500x500")
        settings_window.resizable(True, True)
        settings_window.transient(self)  # Make window modal
        settings_window.grab_set()
        
        # Create a notebook for tabbed settings
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === General Settings Tab ===
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        # Create variables to store settings
        theme_var = tk.StringVar(value="system")  # Default theme
        font_size_var = tk.IntVar(value=10)  # Default font size
        word_wrap_var = tk.BooleanVar(value=False)  # Default word wrap
        show_line_numbers_var = tk.BooleanVar(value=True)  # Default line numbers
        
        # Theme selection
        ttk.Label(general_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        theme_combobox = ttk.Combobox(general_frame, textvariable=theme_var, 
                                    values=["system", "light", "dark"])
        theme_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        # Font size selection
        ttk.Label(general_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        font_spinbox = ttk.Spinbox(general_frame, from_=6, to=24, textvariable=font_size_var)
        font_spinbox.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        # Word wrap option
        word_wrap_check = ttk.Checkbutton(general_frame, text="Word Wrap", variable=word_wrap_var)
        word_wrap_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        
        # Show line numbers option
        line_numbers_check = ttk.Checkbutton(general_frame, text="Show Line Numbers", 
                                            variable=show_line_numbers_var)
        line_numbers_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        
        # === File Types Tab ===
        file_types_frame = ttk.Frame(notebook)
        notebook.add(file_types_frame, text="File Types")
        
        # List of file extensions to monitor
        ttk.Label(file_types_frame, text="Monitored File Extensions:").grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        file_extensions_text = tk.Text(file_types_frame, width=40, height=10, wrap=tk.WORD)
        file_extensions_text.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)
        file_extensions_text.insert(tk.END, ".py\n.js\n.html\n.css\n.java\n.cpp\n.c\n.h\n.cs\n.php")
        
        file_types_frame.columnconfigure(0, weight=1)
        file_types_frame.rowconfigure(1, weight=1)
        
        # Description
        ttk.Label(file_types_frame, text="Add one extension per line (include the dot)").grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10)
        
        # === Context Format Tab ===
        format_frame = ttk.Frame(notebook)
        notebook.add(format_frame, text="Context Format")
        
        # Context format settings
        ttk.Label(format_frame, text="File Header Format:").grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10)
        file_header_entry = ttk.Entry(format_frame, width=40)
        file_header_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        file_header_entry.insert(0, "--- {filename} ---")
        
        ttk.Label(format_frame, text="Selection Header Format:").grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)
        selection_header_entry = ttk.Entry(format_frame, width=40)
        selection_header_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        selection_header_entry.insert(0, "Selection {index}:")
        
        ttk.Label(format_frame, text="Whole File Text:").grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10)
        whole_file_entry = ttk.Entry(format_frame, width=40)
        whole_file_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        whole_file_entry.insert(0, "Archivo completo incluido")
        
        # === Advanced Tab ===
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        
        # Number of recent folders to remember
        ttk.Label(advanced_frame, text="Number of recent folders:").grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10)
        recent_folders_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=20)
        recent_folders_spinbox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        recent_folders_spinbox.insert(0, "5")
        
        # Auto-save options
        autosave_var = tk.BooleanVar(value=False)
        autosave_check = ttk.Checkbutton(advanced_frame, text="Auto-save selections", 
                                        variable=autosave_var)
        autosave_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        
        ttk.Label(advanced_frame, text="Auto-save interval (minutes):").grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10)
        autosave_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=60)
        autosave_spinbox.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        autosave_spinbox.insert(0, "5")
        
        # Token estimation method
        ttk.Label(advanced_frame, text="Token estimation method:").grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=10)
        token_method_combobox = ttk.Combobox(advanced_frame, 
                                            values=["Simple (chars/4)", "Advanced"])
        token_method_combobox.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        token_method_combobox.current(0)
        
        # Configure expansion
        for tab_frame in [general_frame, file_types_frame, format_frame, advanced_frame]:
            tab_frame.columnconfigure(1, weight=1)
        
        # === Buttons frame ===
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save function
        def save_settings():
            try:
                # Create settings dictionary
                settings = {
                    'general': {
                        'theme': theme_var.get(),
                        'font_size': font_size_var.get(),
                        'word_wrap': word_wrap_var.get(),
                        'show_line_numbers': show_line_numbers_var.get()
                    },
                    'file_types': {
                        'extensions': [ext.strip() for ext in file_extensions_text.get(1.0, tk.END).split('\n') 
                                    if ext.strip()]
                    },
                    'format': {
                        'file_header': file_header_entry.get(),
                        'selection_header': selection_header_entry.get(),
                        'whole_file_text': whole_file_entry.get()
                    },
                    'advanced': {
                        'recent_folders_count': int(recent_folders_spinbox.get()),
                        'autosave': autosave_var.get(),
                        'autosave_interval': int(autosave_spinbox.get()),
                        'token_method': token_method_combobox.get()
                    }
                }
                
                # Save settings to json file
                import json
                config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
                os.makedirs(config_dir, exist_ok=True)
                
                settings_file = os.path.join(config_dir, "app_settings.json")
                with open(settings_file, 'w') as f:
                    json.dump(settings, f, indent=2)
                
                # Apply settings
                self._apply_settings(settings)
                
                messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
                settings_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save settings: {str(e)}")
        
        # Load existing settings
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            settings_file = os.path.join(config_dir, "app_settings.json")
            
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)
                
                # Apply loaded settings to the UI
                if 'general' in saved_settings:
                    gen = saved_settings['general']
                    if 'theme' in gen:
                        theme_var.set(gen['theme'])
                    if 'font_size' in gen:
                        font_size_var.set(gen['font_size'])
                    if 'word_wrap' in gen:
                        word_wrap_var.set(gen['word_wrap'])
                    if 'show_line_numbers' in gen:
                        show_line_numbers_var.set(gen['show_line_numbers'])
                
                if 'file_types' in saved_settings and 'extensions' in saved_settings['file_types']:
                    file_extensions_text.delete(1.0, tk.END)
                    file_extensions_text.insert(1.0, '\n'.join(saved_settings['file_types']['extensions']))
                
                if 'format' in saved_settings:
                    fmt = saved_settings['format']
                    if 'file_header' in fmt:
                        file_header_entry.delete(0, tk.END)
                        file_header_entry.insert(0, fmt['file_header'])
                    if 'selection_header' in fmt:
                        selection_header_entry.delete(0, tk.END)
                        selection_header_entry.insert(0, fmt['selection_header'])
                    if 'whole_file_text' in fmt:
                        whole_file_entry.delete(0, tk.END)
                        whole_file_entry.insert(0, fmt['whole_file_text'])
                
                if 'advanced' in saved_settings:
                    adv = saved_settings['advanced']
                    if 'recent_folders_count' in adv:
                        recent_folders_spinbox.delete(0, tk.END)
                        recent_folders_spinbox.insert(0, str(adv['recent_folders_count']))
                    if 'autosave' in adv:
                        autosave_var.set(adv['autosave'])
                    if 'autosave_interval' in adv:
                        autosave_spinbox.delete(0, tk.END)
                        autosave_spinbox.insert(0, str(adv['autosave_interval']))
                    if 'token_method' in adv:
                        token_method_combobox.set(adv['token_method'])
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
        
        # Add buttons
        save_button = ttk.Button(button_frame, text="Save", command=save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Cancel", 
                                command=settings_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Add a restore defaults button
        def restore_defaults():
            if messagebox.askyesno("Restore Defaults", 
                                "Are you sure you want to restore default settings?"):
                # Reset all fields to default values
                theme_var.set("system")
                font_size_var.set(10)
                word_wrap_var.set(False)
                show_line_numbers_var.set(True)
                
                file_extensions_text.delete(1.0, tk.END)
                file_extensions_text.insert(tk.END, ".py\n.js\n.html\n.css\n.java\n.cpp\n.c\n.h\n.cs\n.php")
                
                file_header_entry.delete(0, tk.END)
                file_header_entry.insert(0, "--- {filename} ---")
                
                selection_header_entry.delete(0, tk.END)
                selection_header_entry.insert(0, "Selection {index}:")
                
                whole_file_entry.delete(0, tk.END)
                whole_file_entry.insert(0, "Archivo completo incluido")
                
                recent_folders_spinbox.delete(0, tk.END)
                recent_folders_spinbox.insert(0, "5")
                
                autosave_var.set(False)
                autosave_spinbox.delete(0, tk.END)
                autosave_spinbox.insert(0, "5")
                
                token_method_combobox.current(0)
        
        defaults_button = ttk.Button(button_frame, text="Restore Defaults", 
                                    command=restore_defaults)
        defaults_button.pack(side=tk.LEFT, padx=5)

    def _apply_settings(self, settings):
        """Apply loaded settings to the application."""
        try:
            # Apply theme
            if 'general' in settings and 'theme' in settings['general']:
                theme = settings['general']['theme']
                if theme in ["light", "dark"]:
                    style = ttk.Style()
                    style.theme_use("clam")  # Base theme
                    
                    # Define colors based on theme
                    if theme == "light":
                        bg_color = "#F8F8F8"         # Fondo principal más claro
                        fg_color = "#333333"         # Texto más suave que negro puro
                        select_bg = "#0078D7"        # Azul de selección
                        select_fg = "#FFFFFF"        # Texto en selección
                        tree_bg = "#FFFFFF"          # Fondo del árbol
                        text_bg = "#FFFFFF"          # Fondo del texto
                        text_fg = "#333333"          # Color de texto
                        frame_bg = "#F0F0F0"         # Fondo de marcos
                        button_bg = "#FFFFFF"        # Fondo de botones (blanco)
                        button_fg = "#333333"        # Texto de botones
                        border_color = "#DDDDDD"     # Bordes más suaves
                        highlight_color = "#FFEFBA"  # Amarillo muy claro para resaltados
                    else:  # dark
                        bg_color = "#282828"         # Fondo principal más oscuro
                        fg_color = "#E0E0E0"         # Texto más suave que blanco puro
                        select_bg = "#3A3D41"        # Selección más sutil
                        select_fg = "#FFFFFF"        # Texto en selección
                        tree_bg = "#252525"          # Fondo del árbol ligeramente más oscuro
                        text_bg = "#252525"          # Fondo del texto
                        text_fg = "#E0E0E0"          # Color de texto
                        frame_bg = "#1E1E1E"         # Fondo de marcos
                        button_bg = "#333333"        # Fondo de botones
                        button_fg = "#E0E0E0"        # Texto de botones
                        border_color = "#3F3F3F"     # Bordes más visibles
                        highlight_color = "#3A3A35"  # Color de resaltado mejorado
                    
                    # Configure ttk styles for a minimalist, rounded look
                    
                    # Estilos generales
                    style.configure(".", 
                                background=bg_color, 
                                foreground=fg_color, 
                                bordercolor=border_color,
                                focuscolor=select_bg)
                    
                    # Frames con bordes redondeados
                    style.configure("TFrame", 
                                background=frame_bg, 
                                borderwidth=1, 
                                relief="flat")
                    
                    # LabelFrames con bordes redondeados
                    style.configure("TLabelFrame", 
                                background=frame_bg, 
                                borderwidth=1, 
                                relief="groove")
                    
                    style.configure("TLabelFrame.Label", 
                                background=frame_bg, 
                                foreground=fg_color,
                                font=("Segoe UI", 9, "normal"))
                    
                    # Botones modernos y redondeados
                    style.configure("TButton", 
                                background=button_bg, 
                                foreground=button_fg, 
                                bordercolor=border_color,
                                relief="flat",
                                borderwidth=0,
                                padding=(10, 5),
                                font=("Segoe UI", 9, "normal"))
                    
                    # Efecto hover para botones
                    style.map("TButton",
                            background=[("active", select_bg), ("pressed", select_bg)],
                            foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")],
                            relief=[("active", "flat"), ("pressed", "flat")])
                    
                    # Labels
                    style.configure("TLabel", 
                                background=bg_color, 
                                foreground=fg_color,
                                font=("Segoe UI", 9, "normal"))
                    
                    # Entradas
                    style.configure("TEntry", 
                                background=text_bg, 
                                foreground=text_fg, 
                                fieldbackground=text_bg, 
                                bordercolor=border_color,
                                padding=5,
                                font=("Segoe UI", 9, "normal"))
                    
                    # Checkbuttons
                    style.configure("TCheckbutton", 
                                background=bg_color, 
                                foreground=fg_color,
                                font=("Segoe UI", 9, "normal"))
                    
                    # Notebook (pestañas)
                    style.configure("TNotebook", 
                                background=bg_color, 
                                bordercolor=border_color,
                                tabmargins=[2, 5, 2, 0])
                    
                    style.configure("TNotebook.Tab", 
                                background=button_bg, 
                                foreground=button_fg, 
                                bordercolor=border_color,
                                padding=[10, 4],
                                font=("Segoe UI", 9, "normal"))
                    
                    style.map("TNotebook.Tab",
                            background=[("selected", bg_color), ("active", select_bg)],
                            foreground=[("selected", fg_color), ("active", "#FFFFFF")],
                            expand=[("selected", [1, 1, 1, 0])])
                    
                    # Treeview con estilo minimalista
                    style.configure("Treeview", 
                                background=tree_bg, 
                                foreground=text_fg, 
                                fieldbackground=tree_bg, 
                                bordercolor=border_color,
                                borderwidth=0,
                                font=("Segoe UI", 9, "normal"))
                    
                    style.configure("Treeview.Heading", 
                                background=frame_bg,
                                foreground=fg_color,
                                borderwidth=1,
                                relief="flat",
                                font=("Segoe UI", 9, "bold"))
                    
                    style.map("Treeview", 
                            background=[("selected", select_bg)],
                            foreground=[("selected", select_fg)])
                    
                    # Scrollbars minimalistas
                    style.configure("TScrollbar",
                                background=bg_color,
                                bordercolor=bg_color,
                                arrowcolor=button_fg,
                                troughcolor=frame_bg,
                                relief="flat",
                                borderwidth=0)
                    
                    style.map("TScrollbar",
                            background=[("active", button_bg), ("disabled", bg_color)],
                            arrowcolor=[("active", select_bg), ("disabled", button_fg)])
                    
                    # Update all standard widgets in the application
                    # Main window
                    self.configure(background=bg_color)
                    
                    # Update text widgets colors - these are Tk native widgets, not ttk
                    if hasattr(self, 'file_content_panel') and hasattr(self.file_content_panel, 'content_text'):
                        self.file_content_panel.content_text.configure(
                            background=text_bg, 
                            foreground=text_fg,
                            insertbackground=text_fg,  # Cursor color
                            selectbackground=select_bg,
                            selectforeground=select_fg,
                            borderwidth=0,
                            highlightthickness=1,
                            highlightbackground=border_color,
                            highlightcolor=select_bg,
                            font=("Consolas", 10),
                            padx=5,
                            pady=5
                        )
                        # Update highlight tag color
                        self.file_content_panel.content_text.tag_configure(
                            "selection_highlight", 
                            background=highlight_color
                        )
                    
                    if hasattr(self, 'context_panel') and hasattr(self.context_panel, 'context_text'):
                        self.context_panel.context_text.configure(
                            background=text_bg, 
                            foreground=text_fg,
                            insertbackground=text_fg,
                            selectbackground=select_bg,
                            selectforeground=select_fg,
                            borderwidth=0,
                            highlightthickness=1,
                            highlightbackground=border_color,
                            highlightcolor=select_bg,
                            font=("Consolas", 10),
                            padx=5,
                            pady=5
                        )
                        # Update tag colors in context text
                        self.context_panel.context_text.tag_configure(
                            "file_header", 
                            font=("Segoe UI", 10, "bold"),
                            foreground="#0066CC" if theme == "light" else "#77AAFF"
                        )
                        self.context_panel.context_text.tag_configure(
                            "complete_file", 
                            font=("Segoe UI", 9, "italic"), 
                            foreground="#008000" if theme == "light" else "#00BB00"
                        )
                        self.context_panel.context_text.tag_configure(
                            "selection_header", 
                            font=("Segoe UI", 9, "italic"), 
                            foreground="#0066CC" if theme == "light" else "#77AAFF"
                        )
                        self.context_panel.context_text.tag_configure(
                            "selection_highlight", 
                            background=highlight_color
                        )
                    
                    # Update line numbers if they exist
                    if hasattr(self.file_content_panel, 'line_numbers'):
                        self.file_content_panel.line_numbers.configure(
                            background=frame_bg,
                            foreground=text_fg,
                            highlightbackground=border_color,
                            highlightcolor=border_color,
                            borderwidth=0,
                            highlightthickness=0,
                            font=("Consolas", 10)
                        )
                    
                    # Update scrollbars
                    if hasattr(self.file_content_panel, 'content_scrolly'):
                        self._update_scrollbar_colors(self.file_content_panel.content_scrolly, bg_color, text_bg)
                    
                    if hasattr(self.file_content_panel, 'content_scrollx'):
                        self._update_scrollbar_colors(self.file_content_panel.content_scrollx, bg_color, text_bg)
                    
                    if hasattr(self.context_panel, 'context_scrolly'):
                        self._update_scrollbar_colors(self.context_panel.context_scrolly, bg_color, text_bg)
                    
                    if hasattr(self.context_panel, 'context_scrollx'):
                        self._update_scrollbar_colors(self.context_panel.context_scrollx, bg_color, text_bg)
                    
                    # Update tag colors for syntax highlighting
                    if hasattr(self, 'syntax_highlighter'):
                        self.syntax_highlighter.update_theme(theme)
                        
                        # Re-apply syntax highlighting to current file
                        if self.current_file:
                            file_ext = os.path.splitext(self.current_file)[1].lower()
                            current_state = self.file_content_panel.content_text['state']
                            self.file_content_panel.content_text.config(state=tk.NORMAL)
                            self.syntax_highlighter.highlight(self.file_content_panel.content_text, file_ext)
                            self.file_content_panel.content_text.config(state=current_state)
            
            # Apply font size
            if 'general' in settings and 'font_size' in settings['general']:
                font_size = settings['general']['font_size']
                
                # Update font in content and context panels
                font_family = "Consolas"  # Usar Consolas como fuente monoespaciada para el código
                if hasattr(self, 'file_content_panel') and hasattr(self.file_content_panel, 'content_text'):
                    self.file_content_panel.content_text.config(font=(font_family, font_size))
                
                if hasattr(self, 'context_panel') and hasattr(self.context_panel, 'context_text'):
                    self.context_panel.context_text.config(font=(font_family, font_size))
                
                # Update line numbers font if they exist
                if hasattr(self.file_content_panel, 'line_numbers'):
                    self.file_content_panel.line_numbers.config(font=(font_family, font_size))
            
            # Apply word wrap
            if 'general' in settings and 'word_wrap' in settings['general']:
                word_wrap = settings['general']['word_wrap']
                
                # Set word wrap mode
                wrap_mode = tk.WORD if word_wrap else tk.NONE
                if hasattr(self, 'file_content_panel') and hasattr(self.file_content_panel, 'content_text'):
                    self.file_content_panel.content_text.config(wrap=wrap_mode)
                
                if hasattr(self, 'context_panel') and hasattr(self.context_panel, 'context_text'):
                    self.context_panel.context_text.config(wrap=wrap_mode)
            
            # Apply line numbers
            if 'general' in settings and 'show_line_numbers' in settings['general']:
                show_line_numbers = settings['general']['show_line_numbers']
                
                # Create or update line numbers for file content
                if show_line_numbers:
                    if not hasattr(self.file_content_panel, 'line_numbers'):
                        self._setup_line_numbers()
                    else:
                        self.file_content_panel.show_line_numbers = True
                        self.file_content_panel.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
                    self._update_line_numbers()
                else:
                    # Hide line numbers if they exist
                    if hasattr(self.file_content_panel, 'line_numbers'):
                        self.file_content_panel.line_numbers.pack_forget()
                    self.file_content_panel.show_line_numbers = False
            
            # Apply format settings to SelectionManager
            if 'format' in settings:
                fmt = settings['format']
                if hasattr(self, 'selection_manager'):
                    if 'file_header' in fmt:
                        self.selection_manager.file_header_format = fmt['file_header']
                    if 'selection_header' in fmt:
                        self.selection_manager.selection_header_format = fmt['selection_header']
                    if 'whole_file_text' in fmt:
                        self.selection_manager.whole_file_text = fmt['whole_file_text']
            
            # Setup autosave if enabled
            if 'advanced' in settings and 'autosave' in settings['advanced'] and settings['advanced']['autosave']:
                interval_mins = settings['advanced'].get('autosave_interval', 5)
                interval_ms = interval_mins * 60 * 1000
                
                # Cancel existing autosave task if any
                if hasattr(self, '_autosave_task_id') and self._autosave_task_id:
                    self.after_cancel(self._autosave_task_id)
                
                # Define autosave function
                def autosave_task():
                    if hasattr(self, 'selection_manager') and hasattr(self.selection_manager, 'get_all_selections'):
                        if self.selection_manager.get_all_selections():
                            # Only save if there are selections
                            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
                            os.makedirs(config_dir, exist_ok=True)
                            
                            autosave_file = os.path.join(config_dir, "autosave.json")
                            self.selection_manager.save_selections_to_file(autosave_file)
                            print(f"Auto-saved selections to {autosave_file}")
                    
                    # Schedule next autosave
                    self._autosave_task_id = self.after(interval_ms, autosave_task)
                
                # Start autosave task
                self._autosave_task_id = self.after(interval_ms, autosave_task)
                self.update_idletasks()
            
        except Exception as e:
            print(f"Error applying settings: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Intento aplicar un estilo básico en caso de error
            try:
                style = ttk.Style()
                style.theme_use("clam")  # Usar tema clam como base
                
                # Usar colores predeterminados para modo claro
                bg_color = "#F8F8F8"
                fg_color = "#333333"
                
                # Configurar elementos básicos
                style.configure(".", background=bg_color, foreground=fg_color)
                self.configure(background=bg_color)
                
            except Exception as inner_error:
                print(f"Error applying fallback style: {str(inner_error)}")

    def _update_scrollbar_colors(self, scrollbar, bg_color, trough_color):
        """Update scrollbar colors for theme consistency."""
        if isinstance(scrollbar, ttk.Scrollbar):
            # Para las barras de desplazamiento ttk, aplicar estilos predefinidos
            pass
        else:
            # Para barras de desplazamiento tk.Scrollbar
            scrollbar.configure(
                background="#CCCCCC" if bg_color == "#F8F8F8" else "#555555",  # Color del deslizador
                troughcolor=trough_color,  # Color del fondo
                activebackground="#AAAAAA" if bg_color == "#F8F8F8" else "#777777",  # Color al pasar el ratón
                highlightbackground=bg_color,
                relief="flat",
                borderwidth=0,
                width=10  # Barra más ancha para mejor usabilidad
            )

    def _show_about(self):
        """Muestra información sobre la aplicación."""
        messagebox.showinfo(
            "Acerca de",
            "Selector de Contexto para LLMs\n"
            "Versión 1.0\n\n"
            "Aplicación para seleccionar archivos y fragmentos de código "
            "como contexto para modelos de lenguaje durante la programación."
        )

    def _load_settings(self):
        """Loads the saved configuration."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            os.makedirs(config_dir, exist_ok=True)
            
            # Load folder history
            config_file = os.path.join(config_dir, "settings.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    settings = json.load(f)
                
                # Restore last folder
                if "last_folder" in settings and os.path.exists(settings["last_folder"]):
                    self.current_folder = settings["last_folder"]
                    
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
            import traceback
            traceback.print_exc()
        
    def _save_settings(self):
        """Guarda la configuración actual."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            os.makedirs(config_dir, exist_ok=True)
            
            settings = {
                "last_folder": self.current_folder
            }
            
            config_file = os.path.join(config_dir, "settings.json")
            with open(config_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error al guardar configuración: {str(e)}")
            
    def _remove_selected_text(self):
        """Elimina la selección actualmente resaltada en el área de contexto."""
        if hasattr(self, 'current_context_selection'):
            file_path, idx, is_whole_file = self.current_context_selection
            
            if is_whole_file:
                # Si es un archivo completo, eliminarlo completamente
                self.selection_manager.remove_file(file_path)
                
                # Actualizar el estado del checkbox en el árbol
                self._update_checkbox_state(file_path, False)
            else:
                # Si es una selección individual, eliminar solo esa selección
                self.selection_manager.remove_selection(file_path, idx)
            
            # Limpiar la referencia
            delattr(self, 'current_context_selection')
    
    def _show_context_stats(self):
        """Muestra estadísticas sobre el contexto actual."""
        # Obtener estadísticas
        stats = self.selection_manager.get_selection_stats()
        
        if stats['total_files'] == 0:
            messagebox.showinfo("Estadísticas del contexto", "No hay archivos en el contexto.")
            return
        
        # Crear un mensaje con las estadísticas
        message = "Estadísticas del contexto actual:\n\n"
        message += f"Archivos incluidos: {stats['total_files']}\n"
        message += f"    - Archivos completos: {stats['whole_files']}\n"
        message += f"    - Selecciones parciales: {stats['partial_selections']}\n\n"
        message += f"Tamaño total: {stats['total_chars']} caracteres\n"
        message += f"Tokens aproximados: {stats['approx_tokens']}\n"
        
        # Mostrar el diálogo con estadísticas
        messagebox.showinfo("Estadísticas del contexto", message)
        
    def _add_selected_files_to_context(self, selected_items):
        """
        Añade múltiples archivos seleccionados al contexto.
        
        Args:
            selected_items: Lista de IDs de elementos seleccionados en el árbol
        """
        if not selected_items:
            return
        
        # Contadores para estadísticas
        skipped_dirs = 0
        file_paths = []
        
        # Recopilar las rutas de los archivos a añadir
        for item_id in selected_items:
            # Verificar si es un archivo (no directorio)
            item_tags = self.file_tree_panel.file_tree.item(item_id, "tags")
            if "directory" in item_tags:
                skipped_dirs += 1
                continue
            
            # Obtener la ruta completa del archivo
            file_path = self._get_full_path(item_id, self.file_tree_panel.file_tree)
            if file_path and os.path.isfile(file_path):
                file_paths.append((item_id, file_path))
        
        # Procesar los archivos en lote
        if file_paths:
            # Extraer solo las rutas para pasarlas al selection_manager
            paths_only = [path for _, path in file_paths]
            success_count, error_count = self.selection_manager.add_multiple_files(paths_only)
            
            # Actualizar las casillas de verificación para los archivos añadidos
            for item_id, _ in file_paths:
                self.file_tree_panel.file_tree.item(item_id, values=("☑",))
            
            # Mostrar mensaje solo si hay errores
            if error_count > 0:
                messagebox.showerror(
                    "Error al añadir archivos", 
                    f"Se añadieron {success_count} archivos al contexto.\n"
                    f"Se omitieron {skipped_dirs} directorios.\n"
                    f"No se pudieron añadir {error_count} archivos."
                )
        elif skipped_dirs > 0:
            # Mostrar mensaje si solo se seleccionaron directorios
            messagebox.showinfo(
                "Sin cambios", 
                f"No se seleccionaron archivos válidos para añadir.\n"
                f"Se omitieron {skipped_dirs} directorios."
            )
    
