#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para gestionar selecciones de código en el Selector de Contexto.
Encapsula la lógica para gestionar selecciones de archivos y fragmentos de código.
"""

import os

class SelectionManager:
    """Clase que gestiona las selecciones de código y archivos para el contexto."""
    
    def __init__(self):
        """Inicializa el gestor de selecciones."""
        # Diccionario para almacenar selecciones {file_path: [(content, is_whole_file), ...]}
        self.selections = {}  
        # Diccionario para almacenar rangos de selecciones {file_path: [(start1, end1), ...]}
        self.selection_ranges = {}
        # Para notificar cambios (patrón Observer)
        self.observers = []

    def add_observer(self, observer):
        """Añade un observador para notificar cambios en las selecciones."""
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
                observer.update_from_selection_manager()
            except Exception as e:
                self.logger.error(f"Error al notificar observador: {str(e)}")
    
    def add_selection(self, file_path, selection, selection_range=None, is_whole_file=False):
        """
        Añade una selección al contexto.
        
        Args:
            file_path (str): Ruta del archivo
            selection (str): Texto seleccionado
            selection_range (tuple, optional): Tupla (inicio, fin) con las posiciones
            is_whole_file (bool): Indica si es un archivo completo
                
        Returns:
            bool: True si se añadió correctamente, False si ya existía
        """
        try:
            # Verificar si el archivo ya está incluido como archivo completo
            if self.is_whole_file_in_context(file_path):
                return False
            
            # Verificar si ya existe esta selección (evitar duplicados)
            if self.is_selection_duplicate(file_path, selection):
                return False
            
            # Eliminar selecciones contenidas en esta nueva
            self.remove_contained_selections(file_path, selection)
            
            # Inicializar listas si es la primera selección para este archivo
            if file_path not in self.selections:
                self.selections[file_path] = []
                self.selection_ranges[file_path] = []
            
            # Añadir la selección y su rango
            self.selections[file_path].append((selection, is_whole_file))
            if selection_range and not is_whole_file:
                self.selection_ranges[file_path].append(selection_range)
            
            # Notificar a los observadores
            self.notify_observers()
            return True
        except Exception as e:
            print(f"Error en add_selection: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def add_whole_file(self, file_path, content):
        """
        Añade un archivo completo al contexto.
        
        Args:
            file_path (str): Ruta del archivo
            content (str): Contenido del archivo
            
        Returns:
            bool: True si se añadió correctamente
        """
        # Limpiar selecciones previas para este archivo
        if file_path in self.selection_ranges:
            self.selection_ranges[file_path] = []
        
        # Guardar el archivo completo
        self.selections[file_path] = [(content, True)]
        
        # Notificar a los observadores
        self.notify_observers()
        return True
    
    def remove_file(self, file_path):
        """
        Elimina un archivo del contexto.
        
        Args:
            file_path (str): Ruta del archivo a eliminar
        """
        if file_path in self.selections:
            del self.selections[file_path]
        
        if file_path in self.selection_ranges:
            del self.selection_ranges[file_path]
        
        # Notificar a los observadores
        self.notify_observers()
    
    def remove_selection(self, file_path, index):
        """
        Elimina una selección específica.
        
        Args:
            file_path (str): Ruta del archivo
            index (int): Índice de la selección a eliminar
        """
        if file_path in self.selections and index < len(self.selections[file_path]):
            del self.selections[file_path][index]
            
            # También eliminar el rango si existe
            if file_path in self.selection_ranges and index < len(self.selection_ranges[file_path]):
                del self.selection_ranges[file_path][index]
            
            # Si ya no hay selecciones, eliminar la entrada
            if not self.selections[file_path]:
                del self.selections[file_path]
                if file_path in self.selection_ranges:
                    del self.selection_ranges[file_path]
            
            # Notificar a los observadores
            self.notify_observers()
    
    def clear_all(self):
        """Elimina todas las selecciones."""
        self.selections = {}
        self.selection_ranges = {}
        
        # Notificar a los observadores
        self.notify_observers()
    
    def is_whole_file_in_context(self, file_path):
        """
        Comprueba si un archivo completo ya está en el contexto.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            bool: True si el archivo completo ya está en el contexto
        """
        if file_path not in self.selections:
            return False
        
        # Verificar si alguna selección está marcada como archivo completo
        for _, is_whole_file in self.selections[file_path]:
            if is_whole_file:
                return True
        
        return False
    
    def is_selection_duplicate(self, file_path, selection):
        """
        Comprueba si una selección ya existe en el contexto.
        
        Args:
            file_path (str): Ruta del archivo
            selection (str): Texto de la selección
            
        Returns:
            bool: True si la selección ya existe
        """
        if file_path not in self.selections:
            return False
        
        # Verificar si alguna selección tiene exactamente el mismo texto
        for existing_selection, _ in self.selections[file_path]:
            if selection == existing_selection:
                return True
        
        return False
    
    def remove_contained_selections(self, file_path, new_selection):
        """
        Elimina selecciones que estén contenidas dentro de la nueva selección.
        
        Args:
            file_path (str): Ruta del archivo
            new_selection (str): Nueva selección que puede contener a otras
            
        Returns:
            bool: True si se eliminó alguna selección
        """
        if file_path not in self.selections:
            return False
        
        removed_any = False
        indices_to_remove = []
        
        # Identificar selecciones que son subconjuntos de la nueva
        for i, (existing, is_whole_file) in enumerate(self.selections[file_path]):
            # Solo considerar selecciones parciales (no archivos completos)
            if not is_whole_file and existing in new_selection and existing != new_selection:
                indices_to_remove.append(i)
                removed_any = True
        
        # Eliminar de atrás hacia adelante para mantener índices válidos
        for i in sorted(indices_to_remove, reverse=True):
            del self.selections[file_path][i]
            if file_path in self.selection_ranges and i < len(self.selection_ranges[file_path]):
                del self.selection_ranges[file_path][i]
        
        # Si se eliminó alguna, notificar a los observadores
        if removed_any:
            self.notify_observers()
        
        return removed_any
    
    def get_all_selections(self):
        """
        Obtiene todas las selecciones actuales.
        
        Returns:
            dict: Diccionario con todas las selecciones
        """
        return self.selections
    
    def get_selection_ranges(self, file_path):
        """
        Obtiene los rangos de selección para un archivo.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            list: Lista de rangos (inicio, fin) o lista vacía si no hay
        """
        return self.selection_ranges.get(file_path, [])
    
    def get_formatted_context(self):
        """
        Genera una representación formateada del contexto actual.
        
        Returns:
            str: Texto formateado con todas las selecciones
        """
        result = []
        
        for file_path, selections in self.selections.items():
            if selections:
                file_name = os.path.basename(file_path)
                result.append(f"--- {file_name} ---")
                
                # Procesar cada selección
                has_whole_file = False
                
                for i, (selection, is_whole_file) in enumerate(selections):
                    if is_whole_file:
                        has_whole_file = True
                        result.append("Archivo completo incluido\n")
                        result.append(selection)
                        result.append("")  # Línea en blanco
                        break  # Si hay un archivo completo, solo mostramos ese
                
                # Si no hay archivo completo, mostrar las selecciones individuales
                if not has_whole_file:
                    for i, (selection, _) in enumerate(selections):
                        result.append(f"Selección {i+1}:")
                        result.append(selection)
                        result.append("")  # Línea en blanco
        
        return "\n".join(result)
    
    # Agregar en selection_manager.py
def save_selections_to_file(self, file_path):
    """
    Guarda las selecciones actuales en un archivo JSON.
    
    Args:
        file_path (str): Ruta donde guardar
        
    Returns:
        bool: True si se guardó correctamente
    """
    import json
    
    # Crear estructura serializable
    # No podemos guardar los rangos de texto directamente, así que solo guardamos contenido
    data = {}
    for path, selections in self.selections.items():
        # Convertir a lista simple para guardar
        data[path] = [(content, is_whole_file) for content, is_whole_file in selections]
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar selecciones: {e}")
        return False

def load_selections_from_file(self, file_path):
    """
    Carga selecciones desde un archivo JSON.
    
    Args:
        file_path (str): Ruta del archivo a cargar
        
    Returns:
        bool: True si se cargó correctamente
    """
    import json
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Limpiar selecciones actuales
        self.selections = {}
        self.selection_ranges = {}
        
        # Cargar nuevas selecciones
        for path, file_selections in data.items():
            # Verificar que el archivo todavía existe
            if os.path.exists(path):
                self.selections[path] = []
                for content, is_whole_file in file_selections:
                    self.selections[path].append((content, is_whole_file))
                
                # Inicializar lista de rangos vacía (los rangos se reconstruirán al abrir el archivo)
                self.selection_ranges[path] = []
        
        # Notificar a los observadores
        self.notify_observers()
        return True
    except Exception as e:
        print(f"Error al cargar selecciones: {e}")
        return False
    
    
