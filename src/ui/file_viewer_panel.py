import tkinter as tk
from tkinter import ttk
from syntax_highlighter import SyntaxHighlighter

class FileViewerPanel:
    """Panel para mostrar y manipular el contenido de archivos."""
    
    def __init__(self, parent, on_selection_add):
        """Inicializa el panel de visualización de archivos."""
        self.parent = parent
        self.on_selection_add = on_selection_add
        self.highlight_tag = "selection_highlight"
        self.syntax_highlighter = SyntaxHighlighter()
        
        # Frame principal
        self.frame = ttk.LabelFrame(parent, text="Contenido del archivo")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear widget Text con scrollbars
        self.content_scrolly = ttk.Scrollbar(self.frame)
        self.content_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_scrollx = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.content_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.content = tk.Text(
            self.frame,
            wrap=tk.NONE,
            yscrollcommand=self.content_scrolly.set,
            xscrollcommand=self.content_scrollx.set,
            font=("Courier New", 10),
            state=tk.DISABLED
        )
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.content_scrolly.config(command=self.content.yview)
        self.content_scrollx.config(command=self.content.xview)
        
        # Botón para añadir selección
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.add_selection_btn = ttk.Button(
            self.button_frame,
            text="Añadir selección al contexto",
            command=self._on_add_selection
        )
        self.add_selection_btn.pack(side=tk.LEFT, padx=5)
        
        # Menú contextual
        self.context_menu = tk.Menu(self.content, tearoff=0)
        self.context_menu.add_command(
            label="Añadir selección al contexto",
            command=self._on_add_selection
        )
        self.context_menu.add_command(
            label="Copiar",
            command=self._on_copy_selection
        )
        
        # Eventos
        self.content.bind("<Button-3>", self._show_context_menu)
        
        # Configurar tag de resaltado
        self.content.tag_configure(
            self.highlight_tag,
            background="#FFFF99",
            borderwidth=0
        )
    
    def load_file(self, file_path, content):
        """Carga el contenido de un archivo en el visor."""
        self.current_file = file_path
        self.content.config(state=tk.NORMAL)
        self.content.delete(1.0, tk.END)
        self.content.insert(1.0, content)
        
        # Aplicar resaltado de sintaxis
        self.syntax_highlighter.highlight(self.content, file_path)
        
        self.content.config(state=tk.DISABLED)
    
    def clear(self):
        """Limpia el contenido del visor."""
        self.content.config(state=tk.NORMAL)
        self.content.delete(1.0, tk.END)
        self.content.config(state=tk.DISABLED)
        self.current_file = None
    
    def get_selection(self):
        """Obtiene el texto seleccionado actual."""
        try:
            return self.content.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return None
    
    def get_selection_ranges(self):
        """Obtiene los índices de la selección actual."""
        try:
            return (self.content.index(tk.SEL_FIRST), 
                   self.content.index(tk.SEL_LAST))
        except tk.TclError:
            return None
    
    def highlight_region(self, start_pos, end_pos):
        """Resalta una región específica del texto."""
        self.content.tag_add(self.highlight_tag, start_pos, end_pos)
    
    def clear_highlights(self):
        """Elimina todos los resaltados."""
        self.content.tag_remove(self.highlight_tag, "1.0", tk.END)
    
    def _on_add_selection(self):
        """Maneja el evento de añadir selección."""
        if self.on_selection_add:
            self.on_selection_add()
    
    def _on_copy_selection(self):
        """Copia la selección actual al portapapeles."""
        selection = self.get_selection()
        if selection:
            self.clipboard_clear()
            self.clipboard_append(selection)
    
    def _show_context_menu(self, event):
        """Muestra el menú contextual."""
        if self.get_selection():
            self.context_menu.post(event.x_root, event.y_root)