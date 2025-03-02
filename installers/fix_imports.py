#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir las importaciones relativas en todos los archivos del proyecto.
Cambia 'from utils' a 'from src.utils', 'from core' a 'from src.core', etc.
"""

import os
import re

def fix_imports_in_file(file_path):
    """Corrige las importaciones en un archivo Python."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrones a buscar y reemplazar
    patterns = [
        (r'from utils\.', r'from src.utils.'),
        (r'from core\.', r'from src.core.'),
        (r'from gui\.', r'from src.gui.'),
        (r'import utils\.', r'import src.utils.'),
        (r'import core\.', r'import src.core.'),
        (r'import gui\.', r'import src.gui.'),
    ]
    
    # Aplicar reemplazos
    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    # Guardar el archivo si se modificó
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Corregidas importaciones en: {file_path}")
        return True
    
    return False

def process_directory(directory):
    """Procesa recursivamente un directorio."""
    count = 0
    
    for root, dirs, files in os.walk(directory):
        # Saltar directorios específicos
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
        
        # Procesar archivos Python
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    count += 1
    
    return count

if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
    
    print("Corrigiendo importaciones relativas...")
    count = process_directory(src_dir)
    
    if count > 0:
        print(f"\n✅ Se corrigieron importaciones en {count} archivos.")
    else:
        print("\n✅ No se encontraron importaciones relativas para corregir.")
