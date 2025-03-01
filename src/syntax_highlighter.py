#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para implementar resaltado de sintaxis básico en el Selector de Contexto.
"""

import tkinter as tk
import re

class SyntaxHighlighter:
    """Clase para implementar resaltado de sintaxis básico en widgets Text."""
    
    def __init__(self):
        """Inicializa el resaltador de sintaxis con patrones de lenguajes comunes."""
        # Definir patrones de resaltado para diferentes lenguajes
        self.patterns = {
            # Python
            '.py': {
                'keywords': r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b',
                'strings': r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(#.*$)',
                'functions': r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\s*\())',
                'numbers': r'\b(0x[0-9a-fA-F]+|0b[01]+|[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)\b',
                'decorators': r'(@[a-zA-Z_][a-zA-Z0-9_]*)',
                'class_names': r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)',
                'self': r'\b(self|cls)\b',
            },
            # JavaScript
            '.js': {
                'keywords': r'\b(break|case|catch|class|const|continue|debugger|default|delete|do|else|export|extends|false|finally|for|function|if|import|in|instanceof|new|null|return|super|switch|this|throw|true|try|typeof|var|void|while|with|yield|let|static|enum|await|implements|package|protected|interface|private|public)\b',
                'strings': r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'.*?[^\\]\'|\".*?[^\\]\"|\`[\s\S]*?\`)',
                'comments': r'(\/\/.*$|\/\*[\s\S]*?\*\/)',
                'functions': r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\s*\())',
                'numbers': r'\b(0x[0-9a-fA-F]+|0b[01]+|[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)\b',
                'arrow_functions': r'=>',
                'regex': r'\/(?!\/)(?:\[(?:\\.|.)+?\]|\\.|[^\/\\\r\n])+\/[gimuy]*',
                'jsx_tags': r'(<\/?[a-zA-Z][a-zA-Z0-9_\-]*>)',
            },
            # HTML
            '.html': {
                'tags': r'(<\/?[^>]+>)',
                'attributes': r'\s([a-zA-Z_][a-zA-Z0-9_\-]*)(?==)',
                'strings': r'(\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(<!--[\s\S]*?-->)',
                'doctype': r'(<!DOCTYPE[^>]+>)',
                'entities': r'(&[a-zA-Z0-9#]+;)',
            },
            # CSS
            '.css': {
                'selectors': r'([^\{\}]+)(?=\s*\{)',
                'properties': r'([a-zA-Z\-]+)(?=\s*:)',
                'values': r':\s*([^;]+)(?=;)',
                'comments': r'(\/\*[\s\S]*?\*\/)',
                'units': r'(px|em|rem|%|vh|vw|ex|ch|cm|mm|in|pt|pc|fr|deg|grad|rad|turn|s|ms|Hz|kHz|dpi|dpcm|dppx)\b',
                'colors': r'(#[0-9a-fA-F]{3,8}|\brgb\(.*?\)|\brgba\(.*?\)|\bhsl\(.*?\)|\bhsla\(.*?\))',
                'media_queries': r'(@media[^{]+\{)',
            },
            # JSON
            '.json': {
                'keys': r'\"([^\"]+)\"(?=\s*:)',
                'strings': r':\s*\"([^\"]+)\"',
                'numbers': r':\s*([0-9]+(\.[0-9]+)?)',
                'booleans': r':\s*(true|false)',
                'null': r':\s*(null)',
            },
            # Markdown
            '.md': {
                'headers': r'^(#+)\s+(.+)$',
                'emphasis': r'(\*\*[^*]+\*\*|\*[^*]+\*|__[^_]+__|_[^_]+_)',
                'lists': r'^(\s*[\*\-\+]\s+|^\s*[0-9]+\.\s+)(.+)$',
                'blockquotes': r'^(\>\s+)(.+)$',
                'code': r'(`[^`]+`|```[\s\S]*?```)',
                'links': r'(\[.+?\]\(.+?\))',
                'images': r'(!\[.+?\]\(.+?\))',
                'horizontal_rules': r'^(\s*[\*\-\_]{3,}\s*)$',
            },
            # XML
            '.xml': {
                'tags': r'(<\/?[^>]+>)',
                'attributes': r'\s([a-zA-Z_][a-zA-Z0-9_\-:]*)(?==)',
                'strings': r'(\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(<!--[\s\S]*?-->)',
                'cdata': r'(<!\[CDATA\[[\s\S]*?\]\]>)',
                'entities': r'(&[a-zA-Z0-9#]+;)',
            },
            # YAML
            '.yml': {
                'keys': r'^(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*):',
                'lists': r'(\s*-\s+)',
                'strings': r':\s*(\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(#.*$)',
                'booleans': r':\s*(true|false|yes|no|on|off)\b',
                'null': r':\s*(null|~)\b',
            },
            '.yaml': {
                'keys': r'^(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*):',
                'lists': r'(\s*-\s+)',
                'strings': r':\s*(\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(#.*$)',
                'booleans': r':\s*(true|false|yes|no|on|off)\b',
                'null': r':\s*(null|~)\b',
            },
            # SQL
            '.sql': {
                'keywords': r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|AND|OR|NOT|ORDER BY|GROUP BY|HAVING|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN|ON|AS|DISTINCT|COUNT|AVG|SUM|MIN|MAX|BETWEEN|LIKE|IN|CREATE|ALTER|DROP|TABLE|VIEW|INDEX|TRIGGER|PROCEDURE|FUNCTION|DATABASE|SCHEMA|GRANT|REVOKE|COMMIT|ROLLBACK|BEGIN|TRANSACTION)\b',
                'strings': r'(\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(--.*$|\/\*[\s\S]*?\*\/)',
                'numbers': r'\b([0-9]+(\.[0-9]+)?)\b',
                'operators': r'(\+|\-|\*|\/|=|<>|!=|<=|>=|<|>|\|\|)',
            },
            # C/C++
            '.c': {
                'keywords': r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b',
                'strings': r'(\".*?[^\\]\")',
                'comments': r'(\/\/.*$|\/\*[\s\S]*?\*\/)',
                'functions': r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\s*\())',
                'numbers': r'\b([0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)\b',
                'preprocessor': r'(#\s*[a-zA-Z]+)',
            },
            '.cpp': {
                'keywords': r'\b(alignas|alignof|and|and_eq|asm|auto|bitand|bitor|bool|break|case|catch|char|char16_t|char32_t|class|compl|const|constexpr|const_cast|continue|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|not|not_eq|nullptr|operator|or|or_eq|private|protected|public|register|reinterpret_cast|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|true|try|typedef|typeid|typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|xor|xor_eq)\b',
                'strings': r'(\".*?[^\\]\")',
                'comments': r'(\/\/.*$|\/\*[\s\S]*?\*\/)',
                'functions': r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\s*\())',
                'numbers': r'\b([0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?)\b',
                'preprocessor': r'(#\s*[a-zA-Z]+)',
            },
            # Genérico para otros lenguajes
            'default': {
                'keywords': r'\b(if|else|for|while|return|function|class|def|import|export|var|let|const)\b',
                'strings': r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'.*?[^\\]\'|\".*?[^\\]\")',
                'comments': r'(\/\/.*$|\/\*[\s\S]*?\*\/|#.*$)',
                'functions': r'\b([a-zA-Z_][a-zA-Z0-9_]*(?=\s*\())',
                'numbers': r'\b([0-9]+(\.[0-9]+)?)\b',
            }
        }
        
        # Definir colores para los diferentes elementos
        self.colors = {
            'keywords': '#0000FF',     # Azul
            'strings': '#008000',      # Verde
            'comments': '#808080',     # Gris
            'functions': '#800000',    # Marrón
            'numbers': '#FF8000',      # Naranja
            'tags': '#800080',         # Morado
            'attributes': '#FF0000',   # Rojo
            'selectors': '#800080',    # Morado
            'properties': '#FF0000',   # Rojo
            'values': '#0000FF',       # Azul
            'default': '#000000',      # Negro (texto normal)
            'decorators': '#AA6708',   # Naranja oscuro
            'class_names': '#2B91AF',  # Azul verdoso
            'self': '#0000FF',         # Azul (como keywords)
            'arrow_functions': '#FF0000', # Rojo
            'regex': '#FF00FF',        # Magenta
            'jsx_tags': '#800080',     # Morado
            'doctype': '#808080',      # Gris
            'entities': '#FF0000',     # Rojo
            'units': '#FF8000',        # Naranja
            'colors': '#0000FF',       # Azul
            'media_queries': '#800080', # Morado
            'keys': '#FF0000',         # Rojo
            'booleans': '#0000FF',     # Azul
            'null': '#0000FF',         # Azul
            'headers': '#800080',      # Morado
            'emphasis': '#000080',     # Azul marino
            'lists': '#800000',        # Marrón
            'blockquotes': '#808080',  # Gris
            'code': '#008000',         # Verde
            'links': '#0000FF',        # Azul
            'images': '#800080',       # Morado
            'horizontal_rules': '#808080', # Gris
            'cdata': '#808080',        # Gris
            'operators': '#000000',    # Negro
            'preprocessor': '#800080'  # Morado
        }
    
    def highlight(self, text_widget, file_ext):
        """
        Aplica resaltado de sintaxis a un widget Text según la extensión del archivo.
        
        Args:
            text_widget (tk.Text): Widget Text donde aplicar el resaltado
            file_ext (str): Extensión del archivo
        """
        # Habilitar edición temporalmente para aplicar tags
        current_state = text_widget['state']
        text_widget.config(state=tk.NORMAL)
        
        # Obtener el contenido completo
        content = text_widget.get(1.0, tk.END)
        
        # Limpiar tags existentes
        for tag in text_widget.tag_names():
            if tag != "sel":  # Preservar selección
                text_widget.tag_remove(tag, 1.0, tk.END)
        
        # Seleccionar patrones según la extensión
        patterns = self.patterns.get(file_ext.lower(), self.patterns['default'])
        
        # Configurar tags con colores
        for pattern_name, color in self.colors.items():
            text_widget.tag_configure(pattern_name, foreground=color)
        
        # Aplicar patrones
        for pattern_name, pattern in patterns.items():
            self._apply_pattern(text_widget, pattern, pattern_name, content)
        
        # Restaurar estado original
        text_widget.config(state=current_state)
    
    def _apply_pattern(self, text_widget, pattern, tag_name, content):
        """
        Aplica un patrón regex al contenido y marca coincidencias con un tag.
        
        Args:
            text_widget (tk.Text): Widget Text donde aplicar el patrón
            pattern (str): Patrón regex a buscar
            tag_name (str): Nombre del tag a aplicar
            content (str): Contenido del texto
        """
        start_pos = 0
        
        try:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_index = match.start()
                end_index = match.end()
                
                # Caso especial para class_names ya que eliminamos el look-behind
                if tag_name == "class_names" and pattern.startswith(r'\bclass\s+'):
                    # Ajustar índices para que solo aplique el tag al nombre de la clase, no a 'class '
                    start_groups = match.start(1) if match.groups() else match.start()
                    end_groups = match.end(1) if match.groups() else match.end()
                    if start_groups > start_index:  # Si hay grupo capturado
                        start_index = start_groups
                        end_index = end_groups
                
                # Convertir posición de índice a "línea.columna"
                start_line = content[:start_index].count('\n') + 1
                start_col = start_index - content[:start_index].rfind('\n') - 1
                if start_line == 1:
                    start_col = start_index
                
                end_line = content[:end_index].count('\n') + 1
                end_col = end_index - content[:end_index].rfind('\n') - 1
                if end_line == 1:
                    end_col = end_index
                
                # Aplicar tag
                start_mark = f"{start_line}.{start_col}"
                end_mark = f"{end_line}.{end_col}"
                
                try:
                    text_widget.tag_add(tag_name, start_mark, end_mark)
                except Exception:
                    # Manejar errores en caso de índices inválidos
                    pass
        except Exception as e:
            print(f"Error al aplicar patrón '{tag_name}': {str(e)}")
            pass  # Continuar con otros patrones si hay un error
        
    def update_theme(self, theme):
        """
        Update syntax highlighting colors based on the theme.
        
        Args:
            theme (str): Theme name ('light' or 'dark')
        """
        if theme == "dark":
            # Dark theme colors
            self.colors = {
                'keywords': '#569CD6',     # Light blue
                'strings': '#CE9178',      # Light orange/brown
                'comments': '#6A9955',     # Green
                'functions': '#DCDCAA',    # Yellow
                'numbers': '#B5CEA8',      # Light green
                'tags': '#D7BA7D',         # Gold
                'attributes': '#9CDCFE',   # Light blue
                'selectors': '#D7BA7D',    # Gold
                'properties': '#9CDCFE',   # Light blue
                'values': '#CE9178',       # Light orange/brown
                'default': '#D4D4D4',      # Light gray (text normal)
                'decorators': '#C586C0',   # Pink
                'class_names': '#4EC9B0',  # Teal
                'self': '#569CD6',         # Light blue (like keywords)
                'arrow_functions': '#C586C0', # Pink
                'regex': '#D16969',        # Red
                'jsx_tags': '#D7BA7D',     # Gold
                'doctype': '#6A9955',      # Green
                'entities': '#D7BA7D',     # Gold
                'units': '#B5CEA8',        # Light green
                'colors': '#4EC9B0',       # Teal
                'media_queries': '#C586C0', # Pink
                'keys': '#9CDCFE',         # Light blue
                'booleans': '#569CD6',     # Light blue
                'null': '#569CD6',         # Light blue
                'headers': '#C586C0',      # Pink
                'emphasis': '#D4D4D4',     # Light gray
                'lists': '#DCDCAA',        # Yellow
                'blockquotes': '#6A9955',  # Green
                'code': '#CE9178',         # Light orange/brown
                'links': '#9CDCFE',        # Light blue
                'images': '#C586C0',       # Pink
                'horizontal_rules': '#6A9955', # Green
                'cdata': '#6A9955',        # Green
                'operators': '#D4D4D4',    # Light gray
                'preprocessor': '#C586C0'  # Pink
            }
        else:
            # Light theme colors (default)
            self.colors = {
                'keywords': '#0000FF',     # Blue
                'strings': '#008000',      # Green
                'comments': '#808080',     # Gray
                'functions': '#800000',    # Brown
                'numbers': '#FF8000',      # Orange
                'tags': '#800080',         # Purple
                'attributes': '#FF0000',   # Red
                'selectors': '#800080',    # Purple
                'properties': '#FF0000',   # Red
                'values': '#0000FF',       # Blue
                'default': '#000000',      # Black (text normal)
                'decorators': '#AA6708',   # Dark orange
                'class_names': '#2B91AF',  # Teal
                'self': '#0000FF',         # Blue (like keywords)
                'arrow_functions': '#FF0000', # Red
                'regex': '#FF00FF',        # Magenta
                'jsx_tags': '#800080',     # Purple
                'doctype': '#808080',      # Gray
                'entities': '#FF0000',     # Red
                'units': '#FF8000',        # Orange
                'colors': '#0000FF',       # Blue
                'media_queries': '#800080', # Purple
                'keys': '#FF0000',         # Red
                'booleans': '#0000FF',     # Blue
                'null': '#0000FF',         # Blue
                'headers': '#800080',      # Purple
                'emphasis': '#000080',     # Navy
                'lists': '#800000',        # Brown
                'blockquotes': '#808080',  # Gray
                'code': '#008000',         # Green
                'links': '#0000FF',        # Blue
                'images': '#800080',       # Purple
                'horizontal_rules': '#808080', # Gray
                'cdata': '#808080',        # Gray
                'operators': '#000000',    # Black
                'preprocessor': '#800080'  # Purple
            }