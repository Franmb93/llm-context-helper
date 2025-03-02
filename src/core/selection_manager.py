#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para gestionar selecciones de código en el Selector de Contexto.
Encapsula la lógica para gestionar selecciones de archivos y fragmentos de código.
"""

import os
import json

class SelectionManager:
    """Clase que gestiona las selecciones de código y archivos para el contexto."""
    
    def __init__(self, instruction_manager=None):
        """Inicializa el gestor de selecciones."""
        # Diccionario para almacenar selecciones {file_path: [(content, is_whole_file), ...]}
        self.selections = {}  
        # Diccionario para almacenar rangos de selecciones {file_path: [(start1, end1), ...]}
        self.selection_ranges = {}
        # Para notificar cambios (patrón Observer)
        self.observers = []
        # Gestor de instrucciones extra
        self.instruction_manager = instruction_manager
        
        # Formatos para mostrar los elementos del contexto
        self.file_header_format = "--- {filename} ---"
        self.selection_header_format = "Selección {index}:"
        self.whole_file_text = "Archivo completo incluido"
        self.instruction_header_format = "### INSTRUCCIÓN EXTRA: {name} ###"
    
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
                print(f"Error al notificar observador: {str(e)}")
    
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
    
    def add_multiple_files(self, file_paths):
        """
        Añade múltiples archivos completos al contexto.
        
        Args:
            file_paths (list): Lista de rutas de archivos
            
        Returns:
            tuple: (número de archivos añadidos, número de errores)
        """
        success_count = 0
        error_count = 0
        
        for file_path in file_paths:
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    self.add_whole_file(file_path, content)
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                print(f"Error al añadir archivo {file_path}: {str(e)}")
                error_count += 1
        
        # Solo notificar una vez al final para mejorar rendimiento
        self.notify_observers()
        
        return success_count, error_count
    
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
        """
        if file_path not in self.selections:
            return
        
        indices_to_remove = []
        
        for i, (existing_selection, is_whole_file) in enumerate(self.selections[file_path]):
            if not is_whole_file and existing_selection in new_selection and existing_selection != new_selection:
                indices_to_remove.append(i)
        
        # Eliminar en orden inverso para no afectar los índices
        for i in sorted(indices_to_remove, reverse=True):
            del self.selections[file_path][i]
            if file_path in self.selection_ranges and i < len(self.selection_ranges[file_path]):
                del self.selection_ranges[file_path][i]
    
    def get_selection_ranges(self, file_path):
        """
        Obtiene los rangos de selección para un archivo.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            list: Lista de tuplas (inicio, fin) con las posiciones de selección
        """
        return self.selection_ranges.get(file_path, [])
    
    def get_all_selections(self):
        """
        Obtiene todas las selecciones.
        
        Returns:
            dict: Diccionario de selecciones por archivo
        """
        return self.selections
    
    def get_formatted_context(self):
        """
        Obtiene todo el contexto formateado para exportación.
        
        Returns:
            str: Contexto formateado
        """
        result = []
        
        # Añadir instrucción extra si existe
        if self.instruction_manager and self.instruction_manager.get_current_instruction():
            instruction_name = self.instruction_manager.get_current_instruction()
            instruction_content = self.instruction_manager.get_current_instruction_content()
            
            if instruction_content:
                # Añadir encabezado de instrucción
                header = self.instruction_header_format.replace("{name}", instruction_name)
                result.append(header)
                result.append(instruction_content)
                result.append("")  # Línea en blanco para separar
                result.append("")  # Línea en blanco adicional
        
        # Verificar si hay selecciones
        if not self.selections:
            return "\n".join(result) if result else ""
        
        # Añadir selecciones
        for file_path, file_selections in self.selections.items():
            if file_selections:
                file_name = os.path.basename(file_path)
                
                # Añadir encabezado de archivo
                header = self.file_header_format.replace("{filename}", file_name)
                result.append(header)
                
                # Procesar cada selección
                has_whole_file = False
                
                for i, (selection, is_whole_file) in enumerate(file_selections):
                    if is_whole_file:
                        has_whole_file = True
                        result.append(self.whole_file_text)
                        result.append(selection)
                        result.append("")  # Línea en blanco para separar
                        break  # Si hay un archivo completo, solo mostramos ese
                
                # Si no hay archivo completo, mostrar selecciones individuales
                if not has_whole_file:
                    for i, (selection, _) in enumerate(file_selections):
                        section_header = self.selection_header_format.replace("{index}", str(i+1))
                        result.append(section_header)
                        result.append(selection)
                        result.append("")  # Línea en blanco para separar
                
                result.append("")  # Línea en blanco adicional entre archivos
        
        return "\n".join(result)
    
    def search_in_selections(self, search_text):
        """
        Busca texto en todas las selecciones.
        
        Args:
            search_text (str): Texto a buscar
            
        Returns:
            dict: Diccionario con los resultados de la búsqueda
        """
        results = {}
        
        for file_path, file_selections in self.selections.items():
            file_results = []
            
            for i, (selection, is_whole_file) in enumerate(file_selections):
                if search_text.lower() in selection.lower():
                    # Encontrar la posición de la primera ocurrencia
                    start_pos = selection.lower().find(search_text.lower())
                    end_pos = start_pos + len(search_text)
                    
                    # Agregar a los resultados
                    file_results.append((i, selection, start_pos, end_pos))
            
            if file_results:
                results[file_path] = file_results
        
        return results
    
    def get_selection_stats(self):
        """
        Obtiene estadísticas sobre las selecciones.
        
        Returns:
            dict: Diccionario con estadísticas
        """
        stats = {
            'total_files': 0,
            'whole_files': 0,
            'partial_selections': 0,
            'total_chars': 0,
            'approx_tokens': 0,
            'files': []
        }
        
        for file_path, file_selections in self.selections.items():
            if not file_selections:
                continue
            
            stats['total_files'] += 1
            file_chars = 0
            has_whole_file = False
            
            for selection, is_whole_file in file_selections:
                if is_whole_file:
                    has_whole_file = True
                    stats['whole_files'] += 1
                
                file_chars += len(selection)
            
            if not has_whole_file and file_selections:
                stats['partial_selections'] += 1
            
            stats['total_chars'] += file_chars
            
            # Agregar información del archivo
            stats['files'].append({
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': file_chars,
                'is_whole': has_whole_file,
                'selections': len(file_selections)
            })
        
        # Estimación aproximada de tokens (4 caracteres por token como regla general)
        stats['approx_tokens'] = stats['total_chars'] // 4
        
        return stats
    
    def save_selections_to_file(self, file_path):
        """
        Guarda las selecciones en un archivo JSON.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            data = {}
            
            # Preparar datos para guardado
            for path, selections in self.selections.items():
                data[path] = []
                
                for i, (selection, is_whole_file) in enumerate(selections):
                    selection_data = {
                        'content': selection,
                        'is_whole_file': is_whole_file
                    }
                    
                    # Agregar rangos si existen
                    if path in self.selection_ranges and i < len(self.selection_ranges[path]):
                        start, end = self.selection_ranges[path][i]
                        selection_data['range'] = {
                            'start': start,
                            'end': end
                        }
                    
                    data[path].append(selection_data)
            
            # Guardar en archivo JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar selecciones: {str(e)}")
            return False
    
    def load_selections_from_file(self, file_path):
        """
        Carga selecciones desde un archivo JSON.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Limpiar selecciones actuales
            self.selections = {}
            self.selection_ranges = {}
            
            # Cargar selecciones
            for path, selections in data.items():
                if not os.path.exists(path):
                    continue  # Omitir archivos que ya no existen
                
                self.selections[path] = []
                self.selection_ranges[path] = []
                
                for selection_data in selections:
                    content = selection_data['content']
                    is_whole_file = selection_data.get('is_whole_file', False)
                    
                    self.selections[path].append((content, is_whole_file))
                    
                    # Cargar rango si existe
                    if 'range' in selection_data:
                        range_data = selection_data['range']
                        self.selection_ranges[path].append((range_data['start'], range_data['end']))
                    else:
                        self.selection_ranges[path].append(None)
            
            # Notificar a los observadores
            self.notify_observers()
            
            return True
        except Exception as e:
            print(f"Error al cargar selecciones: {str(e)}")
            return False
