#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo para gestionar instrucciones extra en el Selector de Contexto.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json

class InstructionsDialog(tk.Toplevel):
    """Diálogo para gestionar instrucciones extra."""
    
    def __init__(self, parent, instruction_manager):
        """
        Inicializa el diálogo de instrucciones.
        
        Args:
            parent: Ventana padre
            instruction_manager: Gestor de instrucciones
        """
        super().__init__(parent)
        self.parent = parent
        self.instruction_manager = instruction_manager
        
        # Configuración básica de la ventana
        self.title("Instrucciones Extra")
        self.geometry("800x600")
        self.minsize(600, 400)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Variables
        self.current_name = tk.StringVar()
        self.current_name.set("")
        self.current_content = ""
        self.has_changes = False
        
        # Aplicar el tema actual (claro/oscuro)
        self._apply_theme()
        
        # Crear la interfaz
        self._create_widgets()
        
        # Centrar la ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        # Cargar instrucciones
        self._load_instructions()
    
    def _apply_theme(self):
        """Aplica el tema actual (claro/oscuro) a los widgets."""
        try:
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "config")
            app_settings_file = os.path.join(config_dir, "app_settings.json")
            
            # Valor predeterminado
            theme = "light"
            
            if os.path.exists(app_settings_file):
                with open(app_settings_file, 'r') as f:
                    app_settings = json.load(f)
                    if 'general' in app_settings and 'theme' in app_settings['general']:
                        theme = app_settings['general']['theme']
            
            # Configurar colores según el tema
            if theme == "dark":
                # Tema oscuro
                bg_color = "#333333"
                fg_color = "#FFFFFF"
                text_bg = "#444444"
                text_fg = "#FFFFFF"
                listbox_bg = "#444444"
                listbox_fg = "#FFFFFF"
                combobox_bg = "#444444"
                combobox_fg = "#FFFFFF"
            else:
                # Tema claro
                bg_color = "#F0F0F0"
                fg_color = "#000000"
                text_bg = "#FFFFFF"
                text_fg = "#000000"
                listbox_bg = "#FFFFFF"
                listbox_fg = "#000000"
                combobox_bg = "#FFFFFF"
                combobox_fg = "#000000"
            
            # Guardar los colores para usarlos en los widgets
            self.bg_color = bg_color
            self.fg_color = fg_color
            self.text_bg = text_bg
            self.text_fg = text_fg
            self.listbox_bg = listbox_bg
            self.listbox_fg = listbox_fg
            self.combobox_bg = combobox_bg
            self.combobox_fg = combobox_fg
        except Exception as e:
            print(f"Error al aplicar tema: {str(e)}")  
    
    def _create_widgets(self):
        """Crea los widgets de la interfaz."""
        # Panel principal
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo: lista de instrucciones
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Lista de instrucciones
        instruction_frame = ttk.LabelFrame(left_frame, text="Instrucciones disponibles", padding=5)
        instruction_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(instruction_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox con las instrucciones
        self.instruction_listbox = tk.Listbox(
            instruction_frame,
            width=25,
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            bg=self.listbox_bg,
            fg=self.listbox_fg
        )
        self.instruction_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.instruction_listbox.yview)
        
        # Botones para gestionar instrucciones
        btn_frame = ttk.Frame(left_frame, padding=(0, 5, 0, 0))
        btn_frame.pack(fill=tk.X)
        
        self.add_btn = ttk.Button(btn_frame, text="Nueva", command=self._add_instruction)
        self.add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.rename_btn = ttk.Button(btn_frame, text="Renombrar", command=self._rename_instruction)
        self.rename_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 2))
        
        self.delete_btn = ttk.Button(btn_frame, text="Eliminar", command=self._delete_instruction)
        self.delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        
        # Panel derecho: editor de la instrucción
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Nombre de la instrucción
        name_frame = ttk.Frame(right_frame, padding=(0, 0, 0, 5))
        name_frame.pack(fill=tk.X)
        
        ttk.Label(name_frame, text="Nombre:").pack(side=tk.LEFT)
        
        # Aplicar colores al entry del nombre
        style = ttk.Style()
        style.map('TEntry',
                 fieldbackground=[('readonly', self.text_bg)],
                 foreground=[('readonly', self.text_fg)])
        
        self.name_entry = ttk.Entry(name_frame, textvariable=self.current_name, state="readonly")
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Editor de texto para la instrucción
        editor_frame = ttk.LabelFrame(right_frame, text="Contenido de la instrucción", padding=5)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbars para el editor
        y_scrollbar = ttk.Scrollbar(editor_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Editor de texto
        self.content_text = tk.Text(
            editor_frame,
            wrap=tk.NONE,
            undo=True,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            bg=self.text_bg,
            fg=self.text_fg,
            insertbackground=self.text_fg  # Color del cursor
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)
        
        y_scrollbar.config(command=self.content_text.yview)
        x_scrollbar.config(command=self.content_text.xview)
        
        # Botones de acción
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.X)
        
        # Botón para guardar
        self.save_btn = ttk.Button(action_frame, text="Guardar cambios", command=self._save_current)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón para usar instrucción
        self.use_btn = ttk.Button(action_frame, text="Usar esta instrucción", command=self._use_instruction)
        self.use_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón para no usar ninguna instrucción
        self.no_instruction_btn = ttk.Button(action_frame, text="No usar instrucción", command=self._use_no_instruction)
        self.no_instruction_btn.pack(side=tk.LEFT)
        
        # Botón para cerrar
        self.close_btn = ttk.Button(action_frame, text="Cerrar", command=self._on_close)
        self.close_btn.pack(side=tk.RIGHT)
        
        # Enlazar eventos
        self.instruction_listbox.bind("<<ListboxSelect>>", self._on_instruction_select)
        self.content_text.bind("<<Modified>>", self._on_content_modified)
    
    def _load_instructions(self):
        """Carga las instrucciones en la lista."""
        self.instruction_listbox.delete(0, tk.END)
        
        # Obtener todas las instrucciones
        instruction_names = self.instruction_manager.get_instruction_names()
        current = self.instruction_manager.get_current_instruction()
        
        # Ordenar alfabéticamente
        instruction_names.sort()
        
        # Añadir a la lista
        for name in instruction_names:
            self.instruction_listbox.insert(tk.END, name)
            
            # Si es la instrucción actual, seleccionarla
            if name == current:
                index = instruction_names.index(name)
                self.instruction_listbox.selection_set(index)
                self.instruction_listbox.see(index)
                self._on_instruction_select(None)
    
    def _on_content_modified(self, event=None):
        """Actualiza el estado de cambios cuando se modifica el contenido."""
        if self.content_text.edit_modified():
            # Obtener el contenido actual
            current_content = self.content_text.get(1.0, tk.END).rstrip()
            
            # Verificar si hay cambios
            if current_content != self.current_content:
                self.has_changes = True
            else:
                self.has_changes = False
                
            # Reiniciar el flag de modificación
            self.content_text.edit_modified(False)
    
    def _on_instruction_select(self, event):
        """Maneja la selección de una instrucción en la lista."""
        # Primero guardar cambios pendientes si hay alguna instrucción seleccionada
        if self.current_name.get() and self.has_changes:
            if messagebox.askyesno("Cambios pendientes", 
                                 "¿Desea guardar los cambios en la instrucción actual?"):
                self._save_current()
        
        # Obtener la selección actual
        selection = self.instruction_listbox.curselection()
        if not selection:
            # Limpiar el editor si no hay selección
            self.current_name.set("")
            self.content_text.delete(1.0, tk.END)
            self.current_content = ""
            self.has_changes = False
            self.name_entry.config(state="readonly")
            return
        
        # Obtener el nombre de la instrucción seleccionada
        name = self.instruction_listbox.get(selection[0])
        
        # Actualizar el editor
        self.current_name.set(name)
        self.content_text.delete(1.0, tk.END)
        
        # Cargar el contenido de la instrucción
        content = self.instruction_manager.get_instruction(name)
        if content:
            self.content_text.insert(tk.END, content)
            self.current_content = content
        else:
            self.current_content = ""
        
        # Reiniciar el estado de cambios
        self.has_changes = False
        self.content_text.edit_modified(False)
        
        # Actualizar estado de los botones
        current = self.instruction_manager.get_current_instruction()
        self.use_btn.config(state=tk.NORMAL if name != current else tk.DISABLED)
    
    def _add_instruction(self):
        """Añade una nueva instrucción."""
        # Verificar si hay cambios pendientes en la instrucción actual
        if self.current_name.get() and self.has_changes:
            if messagebox.askyesno("Cambios pendientes", 
                               "\u00bfDesea guardar los cambios en la instrucción actual?"):
                self._save_current()
        
        # Pedir el nombre de la nueva instrucción
        name = simpledialog.askstring("Nueva instrucción", "Nombre de la instrucción:")
        if not name:
            return
        
        # Verificar que no exista ya
        if name in self.instruction_manager.get_instruction_names():
            messagebox.showerror("Error", f"Ya existe una instrucción con el nombre '{name}'")
            return
        
        # Añadir la instrucción como vacía (permite guardar instrucciones vacías)
        self.instruction_manager.instructions[name] = ""
        self.instruction_manager._save_instructions()
        
        # Actualizar la interfaz
        self._load_instructions()
        
        # Seleccionar la nueva instrucción en la lista
        for i in range(self.instruction_listbox.size()):
            if self.instruction_listbox.get(i) == name:
                self.instruction_listbox.selection_clear(0, tk.END)
                self.instruction_listbox.selection_set(i)
                self.instruction_listbox.see(i)
                break
        
        # Preparar el editor
        self.current_name.set(name)
        self.content_text.delete(1.0, tk.END)
        self.current_content = ""
        self.has_changes = False
        
        # Dar foco al área de texto para empezar a editar
        self.content_text.focus_set()
        
        # Actualizar estado de los botones
        current = self.instruction_manager.get_current_instruction()
        self.use_btn.config(state=tk.NORMAL if name != current else tk.DISABLED)
    
    def _rename_instruction(self):
        """Renombra la instrucción seleccionada."""
        # Obtener la selección actual
        selection = self.instruction_listbox.curselection()
        if not selection:
            return
        
        # Obtener el nombre actual de la instrucción
        old_name = self.instruction_listbox.get(selection[0])
        
        # Pedir el nuevo nombre
        new_name = simpledialog.askstring("Renombrar instrucción", 
                                        "Nuevo nombre:", 
                                        initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        
        # Verificar que no exista ya
        if new_name in self.instruction_manager.get_instruction_names():
            messagebox.showerror("Error", f"Ya existe una instrucción con el nombre '{new_name}'")
            return
        
        try:
            # Obtener el contenido actual
            content = self.instruction_manager.instructions.get(old_name, "")
            
            # Añadir la instrucción con el nuevo nombre
            self.instruction_manager.instructions[new_name] = content
            
            # Eliminar la instrucción antigua
            del self.instruction_manager.instructions[old_name]
            
            # Si era la instrucción actual, actualizar la referencia
            if self.instruction_manager.get_current_instruction() == old_name:
                self.instruction_manager.current_instruction = new_name
            
            # Guardar cambios y notificar
            self.instruction_manager._save_instructions()
            self.instruction_manager.notify_observers()
            
            # Actualizar la interfaz
            self._load_instructions()
            
            # Seleccionar la instrucción renombrada
            for i in range(self.instruction_listbox.size()):
                if self.instruction_listbox.get(i) == new_name:
                    self.instruction_listbox.selection_clear(0, tk.END)
                    self.instruction_listbox.selection_set(i)
                    self.instruction_listbox.see(i)
                    
                    # Actualizar el nombre actual
                    self.current_name.set(new_name)
                    self.has_changes = False
                    break
            
            messagebox.showinfo("Instrucción renombrada", 
                             f"La instrucción ha sido renombrada de '{old_name}' a '{new_name}'")
        except Exception as e:
            messagebox.showerror("Error al renombrar", 
                               f"No se pudo renombrar la instrucción: {str(e)}")
    
    def _delete_instruction(self):
        """Elimina la instrucción seleccionada."""
        # Obtener la selección actual
        selection = self.instruction_listbox.curselection()
        if not selection:
            return
        
        # Obtener el nombre de la instrucción
        name = self.instruction_listbox.get(selection[0])
        
        # Confirmar eliminación
        if not messagebox.askyesno("Eliminar instrucción", 
                                 f"¿Está seguro de que desea eliminar la instrucción '{name}'?"):
            return
        
        # Eliminar la instrucción
        self.instruction_manager.remove_instruction(name)
        
        # Actualizar la lista
        self._load_instructions()
        
        # Limpiar el editor
        self.current_name.set("")
        self.content_text.delete(1.0, tk.END)
        self.current_content = ""
        self.has_changes = False
    
    def _save_current(self):
        """Guarda los cambios en la instrucción actual."""
        name = self.current_name.get()
        if not name:
            return
        
        # Obtener el contenido del editor
        content = self.content_text.get(1.0, tk.END).rstrip()
        
        try:
            # Guardar la instrucción directamente en el diccionario
            self.instruction_manager.instructions[name] = content
            self.instruction_manager._save_instructions()
            
            # Notificar observadores
            self.instruction_manager.notify_observers()
            
            # Actualizar el contenido actual
            self.current_content = content
            self.has_changes = False
            
            messagebox.showinfo("Instrucción guardada", f"La instrucción '{name}' ha sido guardada")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar la instrucción: {str(e)}")
    
    def _use_instruction(self):
        """Establece la instrucción actual como la seleccionada."""
        name = self.current_name.get()
        if not name:
            return
        
        # Guardar primero los cambios si hay
        if self.has_changes:
            self._save_current()
        
        # Establecer como instrucción actual
        self.instruction_manager.set_current_instruction(name)
        
        # Actualizar estado de los botones
        self.use_btn.config(state=tk.DISABLED)
        
        messagebox.showinfo("Instrucción seleccionada", 
                          f"La instrucción '{name}' será añadida al inicio del contexto")
    
    def _use_no_instruction(self):
        """No usar ninguna instrucción."""
        # Establecer como instrucción actual
        self.instruction_manager.set_current_instruction(None)
        
        # Actualizar estado de los botones
        if self.current_name.get():
            self.use_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("Sin instrucción", 
                          "No se añadirá ninguna instrucción al contexto")
    
    def _on_close(self):
        """Cierra el diálogo."""
        # Verificar si hay cambios pendientes
        if self.current_name.get() and self.has_changes:
            if messagebox.askyesno("Cambios pendientes", 
                                 "¿Desea guardar los cambios en la instrucción actual?"):
                self._save_current()
        
        self.destroy()

def show_instructions_dialog(parent, instruction_manager):
    """
    Muestra el diálogo de gestión de instrucciones.
    
    Args:
        parent: Ventana padre
        instruction_manager: Gestor de instrucciones
    """
    dialog = InstructionsDialog(parent, instruction_manager)
    parent.wait_window(dialog)
