#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase principal para la aplicación Selector de Contexto para LLMs.
Implementa la interfaz gráfica principal utilizando Tkinter.
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

# Importaciones internas
from src.utils.file_utils import ensure_directory_exists, save_to_file, create_custom_scroll_event
from src.utils.clipboard import copy_to_clipboard
from src.core.file_manager import FileManager
from src.core.selection_manager import SelectionManager
from src.core.instructions.instruction_manager import InstructionManager
from src.utils.syntax_highlighter import SyntaxHighlighter
from src.gui.styling.themes import ThemeManager
from src.gui.styling.icons import IconManager
from src.gui.panels.file_tree_panel import FileTreePanel
from src.gui.panels.content_panel import FileContentPanel
from src.gui.panels.context_panel import ContextPanel
from src.gui.dialogs.instructions_dialog import show_instructions_dialog

class ContextSelectorApp(tk.Tk):
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
        self.instruction_manager = InstructionManager()
        self.selection_manager = SelectionManager(self.instruction_manager)
        self.theme_manager = ThemeManager()
        
        # Registrar como observador
        self.selection_manager.add_observer(self)
        self.instruction_manager.add_observer(self)
        
        # Cargar configuración guardada primero, antes de crear la interfaz
        self._load_settings()
        
        # Establecer un icono y configurar la ventana para que sea más moderna
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets")
        icon_path = os.path.join(assets_dir, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(default=icon_path)
        
        # Establecer padding global
        self.main_padding = 10
        
        # Crear gestor de iconos
        self.icon_manager = IconManager(self.theme_manager)
        
        # Crear la interfaz
        self._create_menu()
        self._create_main_layout()
        
        self.context_panel.set_remove_handler(self._remove_selected_text)
        create_custom_scroll_event(self)
        
        # Aplicar tema configurado
        self._apply_theme()
        
        # Cargar la carpeta anterior si existe
        if self.current_folder:
            self.file_tree_panel.set_current_folder(self.current_folder)
            self._load_files()

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
        
        # Menú Instrucciones
        instructions_menu = tk.Menu(self.menu_bar, tearoff=0)
        instructions_menu.add_command(label="Gestionar instrucciones", command=self._manage_instructions, accelerator="Alt+I")
        instructions_menu.add_separator()
        instructions_menu.add_command(label="Sin instrucción", command=lambda: self.instruction_manager.set_current_instruction(None))
        self.menu_bar.add_cascade(label="Instrucciones", menu=instructions_menu)
        
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
        
        # Atajos para instrucciones
        self.bind("<Alt-i>", lambda event: self._manage_instructions())
    
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
            on_stats=self._show_context_stats,
            on_instructions=self._manage_instructions
        )
        self.right_paned.add(self.context_panel.frame, weight=1)
        
        # Configurar el gestor de instrucciones
        self.context_panel.set_instruction_manager(self.instruction_manager)
    
    def update_from_selection_manager(self):
        """Método callback para el patrón Observer del SelectionManager."""
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
            
    def update_from_instruction_manager(self):
        """Método callback para el patrón Observer del InstructionManager."""
        try:
            # Actualizar el desplegable de instrucciones
            self.context_panel.update_from_instruction_manager()
            
            # Actualizar la visualización del contexto si hay instrucciones
            self._update_context_display()
        except Exception as e:
            print(f"Error en update_from_instruction_manager: {str(e)}")
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
        # Obtener el ícono apropiado
        icon = "file"  
        
        if file_info["type"] == "directory":
            icon = "directory"
        elif "language" in file_info:
            lang = file_info["language"].lower()
            icon = self._get_icon_for_language(lang)
        
        # Set checkbox value - only for files, not directories
        checkbox_value = "☐" if file_info["type"] == "file" else ""
        
        item_id = self.file_tree_panel.file_tree.insert(
            parent, 
            "end", 
            text=file_info["name"],
            values=(checkbox_value,),
            tags=(file_info["type"],),
            image=self.icon_manager.get_icon(icon)
        )
        
        if file_info["type"] == "directory" and "children" in file_info:
            for child in file_info["children"]:
                self._add_file_to_tree(child, item_id)
        
        return item_id
    
    def _get_icon_for_language(self, language):
        """Obtiene el nombre del ícono adecuado para un lenguaje."""
        language_to_icon = {
            "python": "python",
            "javascript": "javascript",
            "js": "javascript",
            "html": "html",
            "css": "css",
            "markdown": "markdown",
            "md": "markdown",
            "json": "json",
            "xml": "xml",
            "text": "text",
            "txt": "text"
        }
        
        return language_to_icon.get(language, "file")
    
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
    
    def _get_full_path(self, item_id, tree):
        """Obtiene la ruta completa de un elemento del árbol."""
        path_parts = []
        
        # Recorrer el árbol hacia arriba para construir la ruta
        current_item = item_id
        while current_item:
            item_text = tree.item(current_item, "text")
            path_parts.insert(0, item_text)
            current_item = tree.parent(current_item)
        
        # Construir la ruta completa
        if self.current_folder:
            full_path = os.path.join(self.current_folder, *path_parts)
            return full_path
        return None
    
    def _load_file_content(self, file_path):
        """Carga el contenido de un archivo en el panel de contenido."""
        try:
            self.current_file = file_path
            self.file_content_panel.load_file(file_path)
            
            # Aplicar resaltado a las selecciones previas (si existen)
            ranges = self.selection_manager.get_selection_ranges(file_path)
            if ranges:
                self.file_content_panel.apply_highlights(ranges)
                
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
        search_text = simpledialog.askstring("Buscar", "Texto a buscar en las selecciones:")
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

    def _show_context_stats(self):
        """Muestra estadísticas sobre el contexto actual."""
        # Obtener estadísticas
        stats = self.selection_manager.get_selection_stats()
        
        # Mostrar usando el diálogo especializado
        from src.gui.dialogs.stats_dialog import show_stats_dialog
        show_stats_dialog(self, stats)
        
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
    
    def _open_settings(self):
        """Abre el diálogo de configuración."""
        from src.gui.dialogs.settings_dialog import open_settings_dialog
        open_settings_dialog(self)
    
    def _show_about(self):
        """Muestra información sobre la aplicación."""
        from src.gui.dialogs.about_dialog import show_about_dialog
        show_about_dialog(self)
        
    def _manage_instructions(self):
        """Abre el diálogo para gestionar instrucciones."""
        show_instructions_dialog(self, self.instruction_manager)

    def _load_settings(self):
        """Carga la configuración guardada."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
            ensure_directory_exists(config_dir)
            
            # Cargar última carpeta visitada
            settings_file = os.path.join(config_dir, "settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Restaurar última carpeta
                if "last_folder" in settings and os.path.exists(settings["last_folder"]):
                    self.current_folder = settings["last_folder"]
            
            # Cargar configuración de temas y preferencias
            app_settings_file = os.path.join(config_dir, "app_settings.json")
            if os.path.exists(app_settings_file):
                with open(app_settings_file, 'r') as f:
                    app_settings = json.load(f)
                
                # Configurar tema
                if 'general' in app_settings and 'theme' in app_settings['general']:
                    theme = app_settings['general']['theme']
                    self.theme_manager.set_theme(theme)
                
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
            import traceback
            traceback.print_exc()
        
    def _save_settings(self):
        """Guarda la configuración actual."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "config")
            ensure_directory_exists(config_dir)
            
            settings = {
                "last_folder": self.current_folder
            }
            
            config_file = os.path.join(config_dir, "settings.json")
            with open(config_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error al guardar configuración: {str(e)}")
            
    def _apply_theme(self):
        """Aplica el tema configurado a todos los componentes."""
        # Aplicar tema a nivel de aplicación
        colors = self.theme_manager.apply_theme(self)
        
        # Actualizar los iconos con el nuevo tema
        self.icon_manager.update_icons()
    
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
