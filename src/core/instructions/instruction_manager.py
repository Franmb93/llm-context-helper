#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de instrucciones extra para el Selector de Contexto para LLMs.
Las instrucciones extra se añaden al inicio del contexto generado.
"""

import os
import json
from src.utils.file_utils import ensure_directory_exists

class InstructionManager:
    """Gestiona las instrucciones extra que se añaden al inicio del contexto."""
    
    def __init__(self):
        """Inicializa el gestor de instrucciones."""
        # Diccionario de instrucciones {name: content}
        self.instructions = {}
        self.current_instruction = None
        self.observers = []
        self.config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "config")
        self.instructions_file = os.path.join(self.config_dir, "instructions.json")
        
        # Cargar instrucciones guardadas
        self._load_instructions()
    
    def add_observer(self, observer):
        """Añade un observador para notificar cambios en las instrucciones."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        """Elimina un observador."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self):
        """Notifica a todos los observadores que ha habido un cambio."""
        for observer in self.observers:
            try:
                observer.update_from_instruction_manager()
            except Exception as e:
                print(f"Error al notificar observador: {str(e)}")
    
    def add_instruction(self, name, content):
        """
        Añade o actualiza una instrucción.
        
        Args:
            name (str): Nombre único de la instrucción
            content (str): Contenido de la instrucción
            
        Returns:
            bool: True si se añadió correctamente
        """
        try:
            if not name or not content:
                return False
            
            self.instructions[name] = content
            self._save_instructions()
            self.notify_observers()
            return True
        except Exception as e:
            print(f"Error al añadir instrucción: {str(e)}")
            return False
    
    def remove_instruction(self, name):
        """
        Elimina una instrucción.
        
        Args:
            name (str): Nombre de la instrucción a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        if name in self.instructions:
            del self.instructions[name]
            
            # Si la instrucción actual era la que se eliminó
            if self.current_instruction == name:
                self.current_instruction = None
            
            self._save_instructions()
            self.notify_observers()
            return True
        return False
    
    def get_instruction(self, name):
        """
        Obtiene el contenido de una instrucción.
        
        Args:
            name (str): Nombre de la instrucción
            
        Returns:
            str: Contenido de la instrucción o None si no existe
        """
        return self.instructions.get(name)
    
    def get_all_instructions(self):
        """
        Obtiene todas las instrucciones.
        
        Returns:
            dict: Diccionario con todas las instrucciones {name: content}
        """
        return self.instructions
    
    def get_instruction_names(self):
        """
        Obtiene los nombres de todas las instrucciones.
        
        Returns:
            list: Lista con los nombres de todas las instrucciones
        """
        return list(self.instructions.keys())
    
    def set_current_instruction(self, name):
        """
        Establece la instrucción actual.
        
        Args:
            name (str): Nombre de la instrucción o None para no usar ninguna
            
        Returns:
            bool: True si se estableció correctamente
        """
        if name is None or name in self.instructions:
            self.current_instruction = name
            self._save_instructions()
            self.notify_observers()
            return True
        return False
    
    def get_current_instruction(self):
        """
        Obtiene el nombre de la instrucción actual.
        
        Returns:
            str: Nombre de la instrucción actual o None si no hay ninguna
        """
        return self.current_instruction
    
    def get_current_instruction_content(self):
        """
        Obtiene el contenido de la instrucción actual.
        
        Returns:
            str: Contenido de la instrucción actual o None si no hay ninguna
        """
        if self.current_instruction:
            return self.instructions.get(self.current_instruction)
        return None
    
    def _load_instructions(self):
        """Carga las instrucciones guardadas desde el archivo JSON."""
        try:
            ensure_directory_exists(self.config_dir)
            
            if os.path.exists(self.instructions_file):
                with open(self.instructions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.instructions = data.get('instructions', {})
                self.current_instruction = data.get('current_instruction')
        except Exception as e:
            print(f"Error al cargar instrucciones: {str(e)}")
            self.instructions = {}
            self.current_instruction = None
    
    def _save_instructions(self):
        """Guarda las instrucciones en el archivo JSON."""
        try:
            ensure_directory_exists(self.config_dir)
            
            data = {
                'instructions': self.instructions,
                'current_instruction': self.current_instruction
            }
            
            with open(self.instructions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error al guardar instrucciones: {str(e)}")
