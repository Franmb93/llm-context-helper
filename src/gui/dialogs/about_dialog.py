#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo 'Acerca de' para la aplicación.
"""
import tkinter as tk
from tkinter import ttk

def show_about_dialog(parent):
    """
    Muestra un diálogo 'Acerca de' con información de la aplicación.
    
    Args:
        parent: Ventana padre
    """
    about_window = tk.Toplevel(parent)
    about_window.title("Acerca de")
    about_window.geometry("400x300")
    about_window.resizable(False, False)
    about_window.transient(parent)  # Hacer la ventana modal
    about_window.grab_set()
    
    # Contenedor principal
    main_frame = ttk.Frame(about_window, padding=(20, 20, 20, 20))
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título de la aplicación
    app_title = ttk.Label(main_frame, text="Selector de Contexto para LLMs", 
                        font=("Segoe UI", 14, "bold"))
    app_title.pack(pady=(0, 10))
    
    # Versión
    version_label = ttk.Label(main_frame, text="Versión 1.0", font=("Segoe UI", 10))
    version_label.pack(pady=(0, 20))
    
    # Descripción
    description = """
    Aplicación para seleccionar archivos y fragmentos de código como 
    contexto para modelos de lenguaje durante la programación.
    
    Esta herramienta facilita la preparación de contexto relevante para 
    consultas a modelos de lenguaje (LLMs), mejorando la calidad y 
    relevancia de las respuestas.
    """
    desc_label = ttk.Label(main_frame, text=description, wraplength=350, 
                         justify=tk.CENTER, font=("Segoe UI", 9))
    desc_label.pack(pady=(0, 20))
    
    # Copyright
    copyright_label = ttk.Label(main_frame, text="© 2024", font=("Segoe UI", 8))
    copyright_label.pack(pady=(20, 0))
    
    # Botón de cierre
    close_button = ttk.Button(main_frame, text="Cerrar", command=about_window.destroy)
    close_button.pack(pady=(20, 0))
    
    # Centrar la ventana en la pantalla
    about_window.update_idletasks()
    width = about_window.winfo_width()
    height = about_window.winfo_height()
    x = (about_window.winfo_screenwidth() // 2) - (width // 2)
    y = (about_window.winfo_screenheight() // 2) - (height // 2)
    about_window.geometry(f"+{x}+{y}")
