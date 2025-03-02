#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo para mostrar estadísticas del contexto.
"""
import tkinter as tk
from tkinter import ttk

def show_stats_dialog(parent, stats):
    """
    Muestra un diálogo con estadísticas del contexto.
    
    Args:
        parent: Ventana padre
        stats (dict): Diccionario con estadísticas del contexto
    """
    if stats['total_files'] == 0:
        from tkinter import messagebox
        messagebox.showinfo("Estadísticas del contexto", "No hay archivos en el contexto.")
        return
    
    stats_window = tk.Toplevel(parent)
    stats_window.title("Estadísticas del contexto")
    stats_window.geometry("400x300")
    stats_window.resizable(True, True)
    stats_window.transient(parent)  # Hacer la ventana modal
    stats_window.grab_set()
    
    # Contenedor principal
    main_frame = ttk.Frame(stats_window, padding=(20, 20, 20, 20))
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    title_label = ttk.Label(main_frame, text="Estadísticas del contexto actual", 
                          font=("Segoe UI", 12, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Crear marco para las estadísticas
    stats_frame = ttk.Frame(main_frame)
    stats_frame.pack(fill=tk.BOTH, expand=True)
    
    # Configurar columnas
    stats_frame.columnconfigure(0, weight=3)
    stats_frame.columnconfigure(1, weight=2)
    
    # Mostrar estadísticas
    row = 0
    
    # Función para agregar una fila de estadística
    def add_stat_row(label_text, value, indent=False, is_header=False):
        nonlocal row
        
        if is_header:
            font = ("Segoe UI", 10, "bold")
        else:
            font = ("Segoe UI", 9)
        
        # Indentación para subcategorías
        prefix = "    " if indent else ""
        
        label = ttk.Label(stats_frame, text=f"{prefix}{label_text}", font=font)
        label.grid(row=row, column=0, sticky=tk.W, pady=3)
        
        value_label = ttk.Label(stats_frame, text=str(value), font=font)
        value_label.grid(row=row, column=1, sticky=tk.E, pady=3)
        
        row += 1
    
    # Agregar categorías principales
    add_stat_row("Archivos incluidos:", stats['total_files'], is_header=True)
    add_stat_row("Archivos completos:", stats['whole_files'], indent=True)
    add_stat_row("Con selecciones parciales:", stats['partial_selections'], indent=True)
    
    # Tamaño total
    row += 1  # Espacio adicional
    add_stat_row("Tamaño total:", f"{stats['total_chars']} caracteres", is_header=True)
    
    # Tokens aproximados
    tokens = stats['approx_tokens']
    token_color = "green" if tokens < 4000 else ("orange" if tokens < 8000 else "red")
    
    token_frame = ttk.Frame(stats_frame)
    token_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=3)
    
    token_label = ttk.Label(token_frame, text="Tokens aproximados:", font=("Segoe UI", 10, "bold"))
    token_label.pack(side=tk.LEFT)
    
    token_value = ttk.Label(token_frame, text=str(tokens), font=("Segoe UI", 10, "bold"))
    token_value.pack(side=tk.RIGHT)
    
    row += 1
    
    # Mostrar archivos individuales si hay un número razonable
    if len(stats.get('files', [])) > 0 and len(stats.get('files', [])) <= 10:
        row += 1  # Espacio adicional
        
        file_list_label = ttk.Label(stats_frame, text="Archivos en el contexto:", 
                                  font=("Segoe UI", 10, "bold"))
        file_list_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 3))
        
        row += 1
        
        for file_info in stats.get('files', []):
            file_name = file_info.get('name', 'Desconocido')
            file_size = file_info.get('size', 0)
            
            file_frame = ttk.Frame(stats_frame)
            file_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=2)
            
            file_icon_label = ttk.Label(file_frame, text="📄")
            file_icon_label.pack(side=tk.LEFT, padx=(5, 3))
            
            file_name_label = ttk.Label(file_frame, text=file_name, font=("Segoe UI", 9))
            file_name_label.pack(side=tk.LEFT)
            
            file_size_label = ttk.Label(file_frame, text=f"{file_size} caracteres", 
                                      font=("Segoe UI", 8))
            file_size_label.pack(side=tk.RIGHT)
            
            row += 1
    
    # Botón de cierre
    close_button = ttk.Button(main_frame, text="Cerrar", command=stats_window.destroy)
    close_button.pack(pady=(20, 0))
    
    # Centrar la ventana en la pantalla
    stats_window.update_idletasks()
    width = stats_window.winfo_width()
    height = stats_window.winfo_height()
    x = (stats_window.winfo_screenwidth() // 2) - (width // 2)
    y = (stats_window.winfo_screenheight() // 2) - (height // 2)
    stats_window.geometry(f"+{x}+{y}")
