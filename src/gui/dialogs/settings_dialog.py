#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo de configuración para la aplicación.
"""
import os
import json
import tkinter as tk
from tkinter import ttk

from src.utils.file_utils import ensure_directory_exists

def open_settings_dialog(parent):
    """
    Abre el diálogo de configuración.
    
    Args:
        parent: Ventana padre
    """
    # Crear ventana de diálogo
    settings_window = tk.Toplevel(parent)
    settings_window.title("Configuración")
    settings_window.geometry("500x500")
    settings_window.resizable(True, True)
    settings_window.transient(parent)  # Hacer la ventana modal
    settings_window.grab_set()
    
    # Crear notebook para pestañas de configuración
    notebook = ttk.Notebook(settings_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # === Pestaña de configuración general ===
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")
    
    # Crear variables para almacenar configuraciones
    theme_var = tk.StringVar(value="system")  # Tema predeterminado
    font_size_var = tk.IntVar(value=10)  # Tamaño de fuente predeterminado
    word_wrap_var = tk.BooleanVar(value=False)  # Word wrap predeterminado
    show_line_numbers_var = tk.BooleanVar(value=True)  # Números de línea predeterminados
    
    # Selección de tema
    ttk.Label(general_frame, text="Tema:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    theme_combobox = ttk.Combobox(general_frame, textvariable=theme_var, 
                                values=["system", "light", "dark"])
    theme_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
    
    # Selección de tamaño de fuente
    ttk.Label(general_frame, text="Tamaño de fuente:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    font_spinbox = ttk.Spinbox(general_frame, from_=6, to=24, textvariable=font_size_var)
    font_spinbox.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
    
    # Opción de ajuste de línea (word wrap)
    word_wrap_check = ttk.Checkbutton(general_frame, text="Ajuste de línea", variable=word_wrap_var)
    word_wrap_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
    
    # Opción de mostrar números de línea
    line_numbers_check = ttk.Checkbutton(general_frame, text="Mostrar números de línea", 
                                        variable=show_line_numbers_var)
    line_numbers_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
    
    # === Pestaña de tipos de archivo ===
    file_types_frame = ttk.Frame(notebook)
    notebook.add(file_types_frame, text="Tipos de archivo")
    
    # Lista de extensiones de archivo a monitorear
    ttk.Label(file_types_frame, text="Extensiones de archivo monitoreadas:").grid(
        row=0, column=0, sticky=tk.W, padx=10, pady=10)
    
    file_extensions_text = tk.Text(file_types_frame, width=40, height=10, wrap=tk.WORD)
    file_extensions_text.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)
    file_extensions_text.insert(tk.END, ".py\n.js\n.html\n.css\n.java\n.cpp\n.c\n.h\n.cs\n.php")
    
    file_types_frame.columnconfigure(0, weight=1)
    file_types_frame.rowconfigure(1, weight=1)
    
    # Descripción
    ttk.Label(file_types_frame, text="Agregar una extensión por línea (incluir el punto)").grid(
        row=2, column=0, sticky=tk.W, padx=10, pady=10)
    
    # === Pestaña de formato de contexto ===
    format_frame = ttk.Frame(notebook)
    notebook.add(format_frame, text="Formato de contexto")
    
    # Configuración de formato de contexto
    ttk.Label(format_frame, text="Formato de encabezado de archivo:").grid(
        row=0, column=0, sticky=tk.W, padx=10, pady=10)
    file_header_entry = ttk.Entry(format_frame, width=40)
    file_header_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
    file_header_entry.insert(0, "--- {filename} ---")
    
    ttk.Label(format_frame, text="Formato de encabezado de selección:").grid(
        row=1, column=0, sticky=tk.W, padx=10, pady=10)
    selection_header_entry = ttk.Entry(format_frame, width=40)
    selection_header_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
    selection_header_entry.insert(0, "Selección {index}:")
    
    ttk.Label(format_frame, text="Texto de archivo completo:").grid(
        row=2, column=0, sticky=tk.W, padx=10, pady=10)
    whole_file_entry = ttk.Entry(format_frame, width=40)
    whole_file_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
    whole_file_entry.insert(0, "Archivo completo incluido")
    
    # === Pestaña avanzada ===
    advanced_frame = ttk.Frame(notebook)
    notebook.add(advanced_frame, text="Avanzado")
    
    # Número de carpetas recientes a recordar
    ttk.Label(advanced_frame, text="Número de carpetas recientes:").grid(
        row=0, column=0, sticky=tk.W, padx=10, pady=10)
    recent_folders_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=20)
    recent_folders_spinbox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
    recent_folders_spinbox.insert(0, "5")
    
    # Opciones de guardado automático
    autosave_var = tk.BooleanVar(value=False)
    autosave_check = ttk.Checkbutton(advanced_frame, text="Guardado automático de selecciones", 
                                    variable=autosave_var)
    autosave_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
    
    ttk.Label(advanced_frame, text="Intervalo de guardado (minutos):").grid(
        row=2, column=0, sticky=tk.W, padx=10, pady=10)
    autosave_spinbox = ttk.Spinbox(advanced_frame, from_=1, to=60)
    autosave_spinbox.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
    autosave_spinbox.insert(0, "5")
    
    # Método de estimación de tokens
    ttk.Label(advanced_frame, text="Método de estimación de tokens:").grid(
        row=3, column=0, sticky=tk.W, padx=10, pady=10)
    token_method_combobox = ttk.Combobox(advanced_frame, 
                                        values=["Simple (caracteres/4)", "Avanzado"])
    token_method_combobox.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
    token_method_combobox.current(0)
    
    # Configurar expansión
    for tab_frame in [general_frame, file_types_frame, format_frame, advanced_frame]:
        tab_frame.columnconfigure(1, weight=1)
    
    # === Marco de botones ===
    button_frame = ttk.Frame(settings_window)
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Función de guardado
    def save_settings():
        try:
            # Crear diccionario de configuración
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
            
            # Guardar configuración en archivo json
            config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config")
            ensure_directory_exists(config_dir)
            
            settings_file = os.path.join(config_dir, "app_settings.json")
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            # Aplicar configuración
            if hasattr(parent, '_apply_theme'):
                parent._apply_theme()
            
            # Notificar al usuario
            from tkinter import messagebox
            messagebox.showinfo("Configuración guardada", "La configuración ha sido guardada correctamente.")
            settings_window.destroy()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {str(e)}")
    
    # Cargar configuración existente
    try:
        config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config")
        settings_file = os.path.join(config_dir, "app_settings.json")
        
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                saved_settings = json.load(f)
            
            # Aplicar configuración cargada a la interfaz
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
        print(f"Error al cargar configuración: {str(e)}")
    
    # Agregar botones
    save_button = ttk.Button(button_frame, text="Guardar", command=save_settings)
    save_button.pack(side=tk.RIGHT, padx=5)
    
    cancel_button = ttk.Button(button_frame, text="Cancelar", 
                            command=settings_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=5)
    
    # Agregar un botón para restaurar valores predeterminados
    def restore_defaults():
        from tkinter import messagebox
        if messagebox.askyesno("Restaurar valores predeterminados", 
                            "¿Está seguro de que desea restaurar la configuración predeterminada?"):
            # Restablecer todos los campos a valores predeterminados
            theme_var.set("system")
            font_size_var.set(10)
            word_wrap_var.set(False)
            show_line_numbers_var.set(True)
            
            file_extensions_text.delete(1.0, tk.END)
            file_extensions_text.insert(tk.END, ".py\n.js\n.html\n.css\n.java\n.cpp\n.c\n.h\n.cs\n.php")
            
            file_header_entry.delete(0, tk.END)
            file_header_entry.insert(0, "--- {filename} ---")
            
            selection_header_entry.delete(0, tk.END)
            selection_header_entry.insert(0, "Selección {index}:")
            
            whole_file_entry.delete(0, tk.END)
            whole_file_entry.insert(0, "Archivo completo incluido")
            
            recent_folders_spinbox.delete(0, tk.END)
            recent_folders_spinbox.insert(0, "5")
            
            autosave_var.set(False)
            autosave_spinbox.delete(0, tk.END)
            autosave_spinbox.insert(0, "5")
            
            token_method_combobox.current(0)
    
    defaults_button = ttk.Button(button_frame, text="Restaurar predeterminados", 
                                command=restore_defaults)
    defaults_button.pack(side=tk.LEFT, padx=5)
