#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase principal para la aplicación Selector de Contexto para LLMs.
"""

import tkinter as tk
from tkinter import ttk
from file_manager import FileManager
from syntax_highlighter import SyntaxHighlighter
from ui.file_tree_panel import FileTreePanel
from ui.file_viewer_panel import FileViewerPanel 
from ui.context_viewer_panel import ContextViewerPanel

class ContextSelector(tk.Tk):
    """Clase principal que implementa la interfaz gráfica del selector de contexto."""
    
    def __init__(self):
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
        
        # Crear la interfaz
        self._create_menu()
        self._create_main_layout()
        
    def _create_menu(self):
        """Crea la barra de menú principal."""
        self.menu_bar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir carpeta", command=self._open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        self.config(menu=self.menu_bar)
        
    def _create_main_layout(self):
        """Crea el diseño principal de la interfaz con paneles."""
        # Panel principal divisible
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo (árbol de archivos)
        self.file_tree = FileTreePanel(
            parent=self.main_paned,
            file_manager=self.file_manager,
            on_file_select=self._on_file_select,
        )
        self.main_paned.add(self.file_tree.frame, weight=1)
        
        # Panel derecho dividido verticalmente
        self.right_paned = ttk.PanedWindow(self.main_paned, orient=tk.VERTICAL)
        self.main_paned.add(self.right_paned, weight=3)
        
        # Panel superior derecho (visor de archivos)
        self.file_viewer = FileViewerPanel(
            parent=self.right_paned,
            syntax_highlighter=self.syntax_highlighter
        )
        self.right_paned.add(self.file_viewer.frame, weight=2)
        
        # Panel inferior derecho (visor de contexto)
        self.context_viewer = ContextViewerPanel(
            parent=self.right_paned
        )
        self.right_paned.add(self.context_viewer.frame, weight=1)
        
    def _open_folder(self):
        """Abre un diálogo para seleccionar una carpeta."""
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.file_tree.load_folder(folder)
            
    def _on_file_select(self, file_path):
        """Maneja la selección de un archivo."""
        self.current_file = file_path
        content = self.file_manager.read_file(file_path)
        self.file_viewer.load_file(content)