#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel para visualizar y navegar por archivos en un árbol jerárquico.
"""
import os
import tkinter as tk
from tkinter import ttk

from src.gui.panels.base_panel import Panel

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
        
        # Crear estilo para el botón de donación
        style = ttk.Style()
        coffee_color = "#FF813F"
        style.configure("Donate.TButton",
                      font=("Segoe UI", 9, "bold"),
                      background=coffee_color,
                      foreground="white")
                      
        # Botón de donación
        self.donate_btn = ttk.Button(
            self.actions_frame,
            text="Buy me a coffee!",
            command=self._open_donation_link,
            style="Donate.TButton"
        )
        self.donate_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
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
    
    def _open_donation_link(self):
        """Abre el enlace de donación en el navegador predeterminado"""
        import webbrowser
        webbrowser.open("https://buymeacoffee.com/betanzosdev")
    
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
    
    def clear_tree(self):
        """Limpia todos los elementos del árbol."""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
