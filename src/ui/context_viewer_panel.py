import tkinter as tk
from tkinter import ttk
from utils import copy_to_clipboard, save_to_file

class ContextViewerPanel:
    """Panel para mostrar y gestionar el contexto seleccionado."""
    
    def __init__(self, parent):
        """Inicializa el panel de contexto."""
        self.parent = parent
        
        # Frame principal
        self.frame = ttk.LabelFrame(parent, text="Contexto seleccionado")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.copy_btn = ttk.Button(
            self.button_frame,
            text="Copiar contexto",
            command=self._copy_context
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(
            self.button_frame,
            text="Guardar contexto",
            command=self._save_context
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            self.button_frame,
            text="Limpiar contexto",
            command=self._clear_context
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Área de texto para el contexto
        self.content_scroll = ttk.Scrollbar(self.frame)
        self.content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content = tk.Text(
            self.frame,
            wrap=tk.WORD,
            yscrollcommand=self.content_scroll.set,
            font=("Courier New", 10),
            height=10
        )
        self.content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.content_scroll.config(command=self.content.yview)
        
        # Menú contextual
        self.context_menu = tk.Menu(self.content, tearoff=0)
        self.context_menu.add_command(
            label="Copiar todo",
            command=self._copy_context
        )
        self.context_menu.add_command(
            label="Guardar en archivo",
            command=self._save_context
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Limpiar todo",
            command=self._clear_context
        )
        
        # Eventos
        self.content.bind("<Button-3>", self._show_context_menu)
        
    def add_context(self, file_path, content, is_whole_file=False):
        """Añade contenido al contexto."""
        # Agregar separador si ya hay contenido
        if self.content.get("1.0", "end-1c"):
            self.content.insert(tk.END, "\n\n")
            
        # Agregar encabezado del archivo
        header = f"# FILE: {file_path}\n"
        if is_whole_file:
            header += "# ARCHIVO COMPLETO\n"
        else:
            header += "# FRAGMENTO SELECCIONADO\n"
            
        self.content.insert(tk.END, header)
        
        # Agregar el contenido
        self.content.insert(tk.END, content)
        
    def clear(self):
        """Limpia todo el contexto."""
        self.content.delete(1.0, tk.END)
        
    def get_context(self):
        """Obtiene todo el contenido del contexto."""
        return self.content.get("1.0", "end-1c")
    
    def _copy_context(self):
        """Copia todo el contexto al portapapeles."""
        context = self.get_context()
        if context:
            copy_to_clipboard(context)
    
    def _save_context(self):
        """Guarda el contexto en un archivo."""
        context = self.get_context()
        if context:
            save_to_file(context)
    
    def _clear_context(self):
        """Limpia todo el contexto."""
        self.clear()
    
    def _show_context_menu(self, event):
        """Muestra el menú contextual."""
        self.context_menu.post(event.x_root, event.y_root)