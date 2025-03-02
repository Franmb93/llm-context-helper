#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase base para todos los paneles de la interfaz de usuario.
"""
import tkinter as tk
from tkinter import ttk

class Panel:
    """Clase base para todos los paneles de la interfaz."""
    
    def __init__(self, parent):
        """
        Inicializa un panel genérico.
        
        Args:
            parent: Widget padre donde se creará este panel
        """
        self.parent = parent
        self.frame = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Método a sobrescribir en las clases derivadas."""
        pass
    
    def pack(self, **kwargs):
        """Empaqueta el frame del panel en su contenedor."""
        if self.frame:
            self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Coloca el frame del panel usando grid."""
        if self.frame:
            self.frame.grid(**kwargs)
    
    def place(self, **kwargs):
        """Coloca el frame del panel usando place."""
        if self.frame:
            self.frame.place(**kwargs)
