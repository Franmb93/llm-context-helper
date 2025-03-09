#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para gestionar archivos y carpetas en el Selector de Contexto.
"""

import os

class FileManager:
    """Clase para gestionar operaciones con archivos y carpetas."""
    
    def __init__(self):
        """Inicializa el gestor de archivos."""
        # Extensiones de archivos de código soportadas
        self.code_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.m': 'Objective-C',
            '.sh': 'Shell',
            '.pl': 'Perl',
            '.sql': 'SQL',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.vue': 'Vue'
        }
        
        # Archivos a ignorar
        self.ignore_files = [
            '.git',
            '__pycache__',
            '.vscode',
            '.idea',
            'node_modules',
            '.DS_Store',
            'venv',
            'env',
            '.env'
        ]
    
    def scan_directory(self, directory):
        """
        Escanea un directorio y devuelve una lista estructurada de archivos y carpetas.
        
        Args:
            directory (str): Ruta del directorio a escanear
                
        Returns:
            list: Lista de diccionarios con información de archivos y carpetas
        """
        # Normalizar la ruta
        directory = os.path.normpath(directory)
        
        result = []
        
        try:        
            # Obtener listado de contenidos del directorio
            entries = os.listdir(directory)
            
            # Ordenar: primero carpetas, luego archivos (alfabéticamente)
            entries.sort()
            directories = [e for e in entries if os.path.isdir(os.path.join(directory, e)) 
                          and e not in self.ignore_files]
            files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
            
            # Procesar primero directorios
            for entry in directories:
                path = os.path.join(directory, entry)
                try:
                    # Escanear subdirectorio recursivamente
                    children = self.scan_directory(path)
                    
                    # Solo añadir directorios que no estén vacíos o que contengan archivos de código
                    if children:
                        result.append({
                            "name": entry,
                            "path": path,
                            "type": "directory",
                            "children": children
                        })
                except PermissionError:
                    # Manejar directorios sin permisos de lectura
                    result.append({
                        "name": entry,
                        "path": path,
                        "type": "directory",
                        "children": [{"name": "<Sin acceso>", "path": "", "type": "error"}]
                    })
            
            # Luego procesar archivos
            for entry in files:
                path = os.path.join(directory, entry)
                ext = os.path.splitext(entry)[1].lower()
                
                # Añadir solo archivos con extensiones de código
                if ext in self.code_extensions:
                    result.append({
                        "name": entry,
                        "path": path,
                        "type": "file",
                        "extension": ext,
                        "language": self.code_extensions.get(ext, "Text")
                    })
        
        except PermissionError:
            # Manejar errores de permiso
            result.append({
                "name": "<Sin acceso>",
                "path": directory,
                "type": "error"
            })
        except Exception as e:
            # Manejar otros errores
            result.append({
                "name": f"<Error: {str(e)}>",
                "path": directory,
                "type": "error"
            })
        
        return result
    
    def is_text_file(self, file_path):
        """
        Determina si un archivo es un archivo de texto que puede ser mostrado.
        
        Args:
            file_path (str): Ruta del archivo a verificar
            
        Returns:
            bool: True si es un archivo de texto, False en caso contrario
        """
        # Verificar por extensión
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.code_extensions:
            return True
        
        # Intentar abrir y leer el archivo como texto
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                # Leer primeros KB para detectar si es binario
                sample = f.read(1024)
                # Si hay caracteres nulos, probablemente es binario
                if '\0' in sample:
                    return False
                return True
        except:
            return False
    
    def get_file_content(self, file_path):
        """
        Lee el contenido de un archivo.
        
        Args:
            file_path (str): Ruta del archivo a leer
            
        Returns:
            str: Contenido del archivo o mensaje de error
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            return f"Error al leer archivo: {str(e)}"

    def get_file_type(self, file_path):
        """
        Determina el tipo/lenguaje de un archivo basado en su extensión.
        
        Args:
            file_path (str): Ruta del archivo
            
        Returns:
            str: Tipo de archivo o 'desconocido' si no se reconoce
        """
        ext = os.path.splitext(file_path)[1].lower()
        return self.code_extensions.get(ext, "Desconocido")
