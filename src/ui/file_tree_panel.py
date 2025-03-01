# src/ui/file_tree_panel.py
import tkinter as tk
from tkinter import ttk

class FileTreePanel:
    """Panel para mostrar y navegar por la estructura de archivos."""
    
    def __init__(self, parent, file_manager, on_file_select, on_checkbox_click):
        """Inicializa el panel del árbol de archivos."""
        self.parent = parent
        self.file_manager = file_manager
        self.on_file_select = on_file_select
        self.on_checkbox_click = on_checkbox_click
        
        # Frame principal
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Selector de carpeta
        self.folder_frame = ttk.Frame(self.frame)
        self.folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.folder_btn = ttk.Button(
            self.folder_frame, 
            text="Seleccionar carpeta",
            command=self._on_folder_button_click
        )
        self.folder_btn.pack(side=tk.LEFT, padx=5)
        
        self.current_folder_var = tk.StringVar(value="Ninguna carpeta seleccionada")
        self.folder_label = ttk.Label(
            self.folder_frame,
            textvariable=self.current_folder_var,
            font=("TkDefaultFont", 9, "italic")
        )
        self.folder_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Árbol de archivos
        self.file_frame = ttk.Frame(self.frame)
        self.file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        self.tree_scroll = ttk.Scrollbar(self.file_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.file_frame,
            yscrollcommand=self.tree_scroll.set,
            columns=("select",),
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree.column("#0", width=250, minwidth=150)
        self.tree.column("select", width=50, minwidth=50, stretch=tk.NO)
        
        self.tree.heading("#0", text="Archivo")
        self.tree.heading("select", text="Incluir")
        
        # Configurar scrollbar
        self.tree_scroll.config(command=self.tree.yview)
        
        # Eventos
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<ButtonRelease-1>", self._on_checkbox_click_internal)
        
        # Icons
        self._create_icons()
        
    def _create_icons(self):
        """Crea los íconos para los diferentes tipos de archivos."""
        self.icons = {}
        base_img = tk.PhotoImage(width=16, height=16)
        
        colors = {
            "directory": "#FFD700",
            "file": "#A9A9A9",
            "python": "#3776AB",
            "javascript": "#F7DF1E",
            "html": "#E34F26",
            "css": "#1572B6",
            "markdown": "#083FA1",
            "json": "#000000",
            "xml": "#F16529",
            "text": "#696969",
        }
        
        for icon_name, color in colors.items():
            icon = tk.PhotoImage(width=16, height=16)
            for y in range(16):
                for x in range(16):
                    if icon_name == "directory":
                        if (2 <= x <= 14 and 4 <= y <= 14) or (5 <= x <= 11 and 2 <= y <= 4):
                            icon.put(color, (x, y))
                    else:
                        if 2 <= x <= 14 and 2 <= y <= 14:
                            if x >= 10 and y <= 6 and x + y <= 16:
                                icon.put("#FFFFFF", (x, y))
                            else:
                                icon.put(color, (x, y))
            self.icons[icon_name] = icon
    
    def _get_icon_for_file(self, file_info):
        """Determina el ícono apropiado para un archivo."""
        if file_info["type"] == "directory":
            return self.icons["directory"]
            
        if "language" in file_info:
            lang = file_info["language"].lower()
            if lang in self.icons:
                return self.icons[lang]
        
        return self.icons["file"]
    
    def load_folder(self, folder_path):
        """Carga una carpeta en el árbol."""
        self.current_folder_var.set(folder_path)
        self.clear()
        
        files = self.file_manager.scan_directory(folder_path)
        for file_info in files:
            self._add_file_to_tree(file_info, "")
    
    def clear(self):
        """Limpia el árbol."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def _add_file_to_tree(self, file_info, parent):
        """Añade un archivo o carpeta al árbol."""
        checkbox_value = "☐" if file_info["type"] == "file" else ""
        
        item_id = self.tree.insert(
            parent,
            "end",
            text=file_info["name"],
            values=(checkbox_value,),
            tags=(file_info["type"],),
            image=self._get_icon_for_file(file_info)
        )
        
        if file_info["type"] == "directory" and "children" in file_info:
            for child in file_info["children"]:
                self._add_file_to_tree(child, item_id)
                
        return item_id
    
    def _on_tree_select(self, event):
        """Maneja la selección de elementos en el árbol."""
        selected = self.tree.selection()
        if not selected:
            return
            
        item_id = selected[0]
        if "file" in self.tree.item(item_id, "tags"):
            file_path = self._get_full_path(item_id)
            if self.on_file_select:
                self.on_file_select(file_path)
    
    def _on_checkbox_click_internal(self, event):
        """Maneja los clics en las casillas de verificación."""
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#1":
                item_id = self.tree.identify_row(event.y)
                if item_id and "file" in self.tree.item(item_id, "tags"):
                    current_state = self.tree.item(item_id, "values")[0]
                    new_state = "☑" if current_state == "☐" else "☐"
                    self.tree.item(item_id, values=(new_state,))
                    
                    if self.on_checkbox_click:
                        file_path = self._get_full_path(item_id)
                        self.on_checkbox_click(file_path, new_state == "☑")
    
    def _get_full_path(self, item_id):
        """Obtiene la ruta completa de un elemento."""
        path_parts = []
        while item_id:
            path_parts.insert(0, self.tree.item(item_id, "text"))
            item_id = self.tree.parent(item_id)
        return os.path.join(self.current_folder_var.get(), *path_parts)
    
    def set_checkbox_state(self, file_path, checked):
        """Actualiza el estado de la casilla para un archivo."""
        item_id = self._find_item_by_path(file_path)
        if item_id:
            self.tree.item(item_id, values=("☑" if checked else "☐",))
    
    def _find_item_by_path(self, file_path):
        """Encuentra un item en el árbol por su ruta."""
        file_name = os.path.basename(file_path)
        
        def search(parent):
            for item_id in self.tree.get_children(parent):
                if self.tree.item(item_id, "text") == file_name:
                    if self._get_full_path(item_id) == file_path:
                        return item_id
                result = search(item_id)
                if result:
                    return result
            return None
            
        return search("")