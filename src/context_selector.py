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
import tkinter.font as tkfont
from file_manager import FileManager
from syntax_highlighter import SyntaxHighlighter
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
        self.selections = {}  # Diccionario para almacenar selecciones {file_path: [selection1, selection2, ...]}
        
        # Inicializar componentes
        self.file_manager = FileManager()
        self.syntax_highlighter = SyntaxHighlighter()
        
        # Añadir la siguiente línea:
        self._create_dummy_icons()
        
        # Crear la interfaz
        self._create_menu()
        self._create_main_layout()
        
        # Cargar configuración guardada
        self._load_settings()
    
    def _create_menu(self):
        """Crea la barra de menú principal."""
        self.menu_bar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir carpeta", command=self._open_folder, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Guardar contexto", command=self._save_context, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit, accelerator="Alt+F4")
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Edición
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Copiar selección", command=self._copy_selection, accelerator="Ctrl+C")
        edit_menu.add_command(label="Añadir selección al contexto", command=self._add_selection, accelerator="Ctrl+A")
        edit_menu.add_separator()
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
        self.bind("<Control-a>", lambda event: self._add_selection())
        self.bind("<Control-l>", lambda event: self._clear_context())
    
    def _create_main_layout(self):
        """Crea el diseño principal de la interfaz con paneles."""
        # Contenedor principal con paneles ajustables
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo (lista de archivos)
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)
        
        # Botón para seleccionar carpeta
        self.folder_frame = ttk.Frame(self.left_frame)
        self.folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.folder_btn = ttk.Button(self.folder_frame, text="Seleccionar carpeta", command=self._open_folder)
        self.folder_btn.pack(side=tk.LEFT, padx=5)
        
        self.current_folder_var = tk.StringVar(value="Ninguna carpeta seleccionada")
        self.folder_label = ttk.Label(self.folder_frame, textvariable=self.current_folder_var, 
                                     font=("TkDefaultFont", 9, "italic"))
        self.folder_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Crear el Treeview para la lista de archivos
        self.file_frame = ttk.Frame(self.left_frame)
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar para el Treeview
        self.file_tree_scroll = ttk.Scrollbar(self.file_frame)
        self.file_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview para mostrar la estructura de archivos
        self.file_tree = ttk.Treeview(self.file_frame, yscrollcommand=self.file_tree_scroll.set)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        self.file_tree_scroll.config(command=self.file_tree.yview)
        
        # Configurar columnas del Treeview
        self.file_tree["columns"] = ("select",)
        self.file_tree.column("#0", width=250, minwidth=150)
        self.file_tree.column("select", width=50, minwidth=50, stretch=tk.NO)
        
        self.file_tree.heading("#0", text="Archivo")
        self.file_tree.heading("select", text="Incluir")
        
        # Vincular evento de selección de archivo
        self.file_tree.bind("<<TreeviewSelect>>", self._on_file_select)
        
        # Panel derecho (contenido del archivo y contexto)
        self.right_paned = ttk.PanedWindow(self.main_paned, orient=tk.VERTICAL)
        self.main_paned.add(self.right_paned, weight=3)
        
        # Panel superior (visualización de archivos)
        self.file_content_frame = ttk.LabelFrame(self.right_paned, text="Contenido del archivo")
        self.right_paned.add(self.file_content_frame, weight=2)
        
        # Crear widget Text con scrollbars
        self.file_content_scrolly = ttk.Scrollbar(self.file_content_frame)
        self.file_content_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_content_scrollx = ttk.Scrollbar(self.file_content_frame, orient=tk.HORIZONTAL)
        self.file_content_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.file_content = tk.Text(
            self.file_content_frame,
            wrap=tk.NONE,
            yscrollcommand=self.file_content_scrolly.set,
            xscrollcommand=self.file_content_scrollx.set,
            font=("Courier New", 10),
            state=tk.DISABLED
        )
        self.file_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.file_content_scrolly.config(command=self.file_content.yview)
        self.file_content_scrollx.config(command=self.file_content.xview)
        
        # Botón para añadir selección al contexto
        self.selection_frame = ttk.Frame(self.file_content_frame)
        self.selection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.add_selection_btn = ttk.Button(self.selection_frame, text="Añadir selección al contexto", 
                                           command=self._add_selection)
        self.add_selection_btn.pack(side=tk.LEFT, padx=5)
        
        # Vincular menú contextual al Text
        self.file_content_menu = tk.Menu(self.file_content, tearoff=0)
        self.file_content_menu.add_command(label="Añadir selección al contexto", command=self._add_selection)
        self.file_content_menu.add_command(label="Copiar", command=self._copy_selection)
        
        self.file_content.bind("<Button-3>", self._show_context_menu)
        
        # Panel inferior (contexto recopilado)
        self.context_frame = ttk.LabelFrame(self.right_paned, text="Contexto seleccionado")
        self.right_paned.add(self.context_frame, weight=1)
        
        # Botones para el contexto
        self.context_btn_frame = ttk.Frame(self.context_frame)
        self.context_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.copy_context_btn = ttk.Button(self.context_btn_frame, text="Copiar al portapapeles", 
                                          command=self._copy_context)
        self.copy_context_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_context_btn = ttk.Button(self.context_btn_frame, text="Guardar contexto", 
                                          command=self._save_context)
        self.save_context_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_context_btn = ttk.Button(self.context_btn_frame, text="Limpiar contexto", 
                                           command=self._clear_context)
        self.clear_context_btn.pack(side=tk.LEFT, padx=5)
        
        # Crear widget Text para el contexto con scrollbars
        self.context_scrolly = ttk.Scrollbar(self.context_frame)
        self.context_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.context_scrollx = ttk.Scrollbar(self.context_frame, orient=tk.HORIZONTAL)
        self.context_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.context_text = tk.Text(
            self.context_frame,
            wrap=tk.NONE,
            yscrollcommand=self.context_scrolly.set,
            xscrollcommand=self.context_scrollx.set,
            font=("Courier New", 10)
        )
        self.context_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.context_scrolly.config(command=self.context_text.yview)
        self.context_scrollx.config(command=self.context_text.xview)
    
    def _open_folder(self):
        """Abre un diálogo para seleccionar una carpeta y la carga en el árbol."""
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder_path:
            self.current_folder = folder_path
            self.current_folder_var.set(folder_path)
            self._load_files()
            self._save_settings()
    
    def _load_files(self):
        """Carga los archivos de la carpeta seleccionada en el Treeview."""
        # Limpiar el árbol actual
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        if not self.current_folder:
            return
        
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
        
        item_id = self.file_tree.insert(
            parent, 
            "end", 
            text=file_info["name"],
            values=("",),
            tags=(file_info["type"],),
            image=self.tree_icons.get(icon, self.tree_icons["file"])
        )
        
        if file_info["type"] == "directory" and "children" in file_info:
            for child in file_info["children"]:
                self._add_file_to_tree(child, item_id)
        
        return item_id
    
    def _on_file_select(self, event):
        """Maneja el evento de selección de un archivo en el árbol."""
        selected_item = self.file_tree.selection()
        if not selected_item:
            return
        
        item_id = selected_item[0]
        item_tags = self.file_tree.item(item_id, "tags")
        
        # Si es un directorio, expandir/colapsar
        if "directory" in item_tags:
            if self.file_tree.item(item_id, "open"):
                self.file_tree.item(item_id, open=False)
            else:
                self.file_tree.item(item_id, open=True)
            return
        
        # Si es un archivo, cargar su contenido
        file_path = self._get_full_path(item_id)
        if file_path:
            self._load_file_content(file_path)
    
    def _get_full_path(self, item_id):
        """Obtiene la ruta completa de un elemento del árbol."""
        path_parts = []
        
        # Recorrer el árbol hacia arriba para construir la ruta
        while item_id:
            item_text = self.file_tree.item(item_id, "text")
            path_parts.insert(0, item_text)
            item_id = self.file_tree.parent(item_id)
        
        # Construir la ruta completa
        full_path = os.path.join(self.current_folder, *path_parts)
        return full_path
    
    def _load_file_content(self, file_path):
        """Carga el contenido de un archivo en el widget Text."""
        try:
            if not os.path.isfile(file_path):
                return
            
            self.current_file = file_path
            
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Actualizar el widget Text
            self.file_content.config(state=tk.NORMAL)
            self.file_content.delete(1.0, tk.END)
            self.file_content.insert(tk.END, content)
            
            # Aplicar resaltado de sintaxis según extensión
            file_ext = os.path.splitext(file_path)[1].lower()
            self.syntax_highlighter.highlight(self.file_content, file_ext)
            
            self.file_content.config(state=tk.DISABLED)
            
            # Actualizar título del frame
            self.file_content_frame.config(text=f"Contenido: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error al cargar archivo", f"No se pudo cargar el archivo: {str(e)}")
    
    def _add_selection(self):
        """Añade la selección actual al contexto."""
        if not self.current_file:
            return
        
        # Obtener la selección actual
        self.file_content.config(state=tk.NORMAL)
        try:
            selection = self.file_content.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showinfo("Sin selección", "No hay texto seleccionado")
            self.file_content.config(state=tk.DISABLED)
            return
        
        self.file_content.config(state=tk.DISABLED)
        
        if not selection:
            return
        
        # Añadir al diccionario de selecciones
        if self.current_file not in self.selections:
            self.selections[self.current_file] = []
        
        self.selections[self.current_file].append(selection)
        
        # Actualizar el área de contexto
        self._update_context_display()
    
    def _update_context_display(self):
        """Actualiza la visualización del contexto seleccionado."""
        self.context_text.config(state=tk.NORMAL)
        self.context_text.delete(1.0, tk.END)
        
        for file_path, selections in self.selections.items():
            if selections:
                file_name = os.path.basename(file_path)
                self.context_text.insert(tk.END, f"--- {file_name} ---\n", "file_header")
                
                for selection in selections:
                    self.context_text.insert(tk.END, selection + "\n\n")
        
        # Configurar tags para el formato
        self.context_text.tag_configure("file_header", font=("TkDefaultFont", 10, "bold"))
        
        self.context_text.config(state=tk.NORMAL)
    
    def _copy_selection(self):
        """Copia la selección actual al portapapeles."""
        try:
            selection = self.file_content.get(tk.SEL_FIRST, tk.SEL_LAST)
            copy_to_clipboard(self, selection)
        except tk.TclError:
            pass
    
    def _copy_context(self):
        """Copia todo el contexto al portapapeles."""
        context = self.context_text.get(1.0, tk.END)
        if context:
            copy_to_clipboard(self, context)
            messagebox.showinfo("Contexto copiado", "El contexto ha sido copiado al portapapeles")
    
    def _save_context(self):
        """Guarda el contexto en un archivo."""
        context = self.context_text.get(1.0, tk.END)
        if not context.strip():
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
            self.selections = {}
            self.context_text.config(state=tk.NORMAL)
            self.context_text.delete(1.0, tk.END)
            self.context_text.config(state=tk.NORMAL)
    
    def _show_context_menu(self, event):
        """Muestra el menú contextual en el área de contenido de archivo."""
        try:
            self.file_content.selection_get()
            self.file_content_menu.tk_popup(event.x_root, event.y_root)
        except:
            pass
        finally:
            self.file_content_menu.grab_release()
    
    def _open_settings(self):
        """Abre el diálogo de configuración."""
        # Aquí iría el código para abrir un diálogo de configuración
        messagebox.showinfo("Configuración", "Funcionalidad en desarrollo")
    
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
        """Carga la configuración guardada."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
            os.makedirs(config_dir, exist_ok=True)
            
            config_file = os.path.join(config_dir, "settings.json")
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    settings = json.load(f)
                
                # Restaurar última carpeta
                if "last_folder" in settings and os.path.exists(settings["last_folder"]):
                    self.current_folder = settings["last_folder"]
                    self.current_folder_var.set(settings["last_folder"])
                    self._load_files()
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
    
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
            

    def _create_dummy_icons(self):
        """Crea íconos temporales hasta que se implementen los íconos reales."""
        # Este método crea íconos básicos para desarrollo, en una aplicación completa
        # deberías tener archivos de imagen reales
        
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