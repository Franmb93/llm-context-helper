#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para resaltado de sintaxis de código.
"""
import re
import tkinter as tk

class SyntaxHighlighter:
    """Clase para resaltar sintaxis en widgets Text de Tkinter."""
    
    def __init__(self):
        """Inicializa el resaltador de sintaxis."""
        # Inicializar tema primero
        self.current_theme = "light"
        # Luego inicializar patrones y tags según lenguaje
        self._init_patterns()
    
    def _init_patterns(self):
        """Inicializa los patrones de resaltado por lenguaje."""
        self.language_patterns = {
            # Python
            '.py': [
                ('keyword', r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b', self._get_color('keyword')),
                ('builtin', r'\b(True|False|None|self|print|input|open|len|range|str|int|float|list|dict|set|tuple)\b', self._get_color('builtin')),
                ('string', r'(\"\"\".*?\"\"\"|\'\'\'.*?\'\'\'|\".*?\"|\'.*?\')', self._get_color('string')),
                ('comment', r'#.*$', self._get_color('comment')),
                ('number', r'\b(0x[0-9a-fA-F]+|\d+\.?\d*|\.\d+)\b', self._get_color('number')),
                ('decorator', r'@\w+', self._get_color('decorator')),
                ('class', r'\bclass\s+(\w+)', self._get_color('class')),
                ('function', r'\bdef\s+(\w+)', self._get_color('function')),
            ],
            
            # JavaScript
            '.js': [
                ('keyword', r'\b(break|case|catch|class|const|continue|debugger|default|delete|do|else|export|extends|finally|for|function|if|import|in|instanceof|new|return|super|switch|this|throw|try|typeof|var|void|while|with|yield|let|static|enum|await|implements|package|protected|interface|private|public)\b', self._get_color('keyword')),
                ('builtin', r'\b(document|window|Array|String|Object|Number|Boolean|Function|Console|Math|Date|RegExp)\b', self._get_color('builtin')),
                ('string', r'(\"\"\".*?\"\"\"|\'\'\'.*?\'\'\'|\".*?\"|\'.*?\'|`.*?`)', self._get_color('string')),
                ('comment', r'(\/\/.*$|\/\*[\s\S]*?\*\/)', self._get_color('comment')),
                ('number', r'\b(0x[0-9a-fA-F]+|\d+\.?\d*|\.\d+)\b', self._get_color('number')),
                ('function', r'\b(\w+)\s*\(', self._get_color('function')),
            ],
            
            # HTML
            '.html': [
                ('tag', r'<\/?[\w\s="/.\':-]*>?', self._get_color('tag')),
                ('attribute', r'\s([\w-]+)="', self._get_color('attribute')),
                ('string', r'"[^"]*"', self._get_color('string')),
                ('comment', r'<!--[\s\S]*?-->', self._get_color('comment')),
            ],
            
            # CSS
            '.css': [
                ('selector', r'[\w\d\s,.#*:>+~[\]()=^$|"\']*\{', self._get_color('selector')),
                ('property', r'\s([\w-]+):', self._get_color('property')),
                ('value', r':\s*(.*?);', self._get_color('value')),
                ('comment', r'\/\*[\s\S]*?\*\/', self._get_color('comment')),
            ],
            
            # JSON
            '.json': [
                ('key', r'"[\w\d_-]*"(?=\s*:)', self._get_color('key')),
                ('string', r':\s*".*?"', self._get_color('string')),
                ('number', r':\s*\b(0x[0-9a-fA-F]+|\d+\.?\d*|\.\d+)\b', self._get_color('number')),
                ('boolean', r':\s*(true|false|null)\b', self._get_color('boolean')),
            ],
            
            # Markdown
            '.md': [
                ('heading1', r'^#\s.*$', self._get_color('heading1')),
                ('heading2', r'^##\s.*$', self._get_color('heading2')),
                ('heading3', r'^###\s.*$', self._get_color('heading3')),
                ('heading4', r'^####\s.*$', self._get_color('heading4')),
                ('bold', r'\*\*.*?\*\*', self._get_color('bold')),
                ('italic', r'\*.*?\*', self._get_color('italic')),
                ('link', r'\[.*?\]\(.*?\)', self._get_color('link')),
                ('code', r'`.*?`', self._get_color('code')),
                ('codeblock', r'```[\s\S]*?```', self._get_color('codeblock')),
                ('quote', r'^>\s.*$', self._get_color('quote')),
                ('list', r'^\s*[\*\-\+]\s.*$', self._get_color('list')),
                ('numlist', r'^\s*\d+\.\s.*$', self._get_color('numlist')),
            ],
        }
    
    def _get_color(self, token_type):
        """
        Obtiene el color adecuado para un tipo de token según el tema.
        
        Args:
            token_type (str): Tipo de token
            
        Returns:
            str: Color en formato hexadecimal
        """
        light_theme_colors = {
            # Colores básicos
            'keyword': '#0000FF',   # Azul
            'builtin': '#7D0252',   # Púrpura
            'string': '#008000',    # Verde
            'comment': '#808080',   # Gris
            'number': '#FF8000',    # Naranja
            'decorator': '#AA5500',  # Naranja oscuro
            'class': '#0000FF',     # Azul
            'function': '#AA0000',  # Rojo oscuro
            
            # HTML/CSS
            'tag': '#008080',       # Verde azulado
            'attribute': '#7D0252', # Púrpura
            'selector': '#800000',  # Marrón
            'property': '#0000FF',  # Azul
            'value': '#008000',     # Verde
            
            # JSON
            'key': '#0000FF',       # Azul
            'boolean': '#008000',   # Verde
            
            # Markdown
            'heading1': '#000080',  # Azul marino
            'heading2': '#000080',  # Azul marino
            'heading3': '#000080',  # Azul marino
            'heading4': '#000080',  # Azul marino
            'bold': '#000000',      # Negro
            'italic': '#000000',    # Negro
            'link': '#0000FF',      # Azul
            'code': '#800000',      # Marrón
            'codeblock': '#800000', # Marrón
            'quote': '#808080',     # Gris
            'list': '#000000',      # Negro
            'numlist': '#000000',   # Negro
        }
        
        dark_theme_colors = {
            # Colores básicos
            'keyword': '#569CD6',   # Azul claro
            'builtin': '#C586C0',   # Púrpura claro
            'string': '#6A9955',    # Verde claro
            'comment': '#6A9955',   # Verde claro
            'number': '#B5CEA8',    # Verde claro
            'decorator': '#DCDCAA',  # Amarillo claro
            'class': '#4EC9B0',     # Verde azulado
            'function': '#DCDCAA',  # Amarillo claro
            
            # HTML/CSS
            'tag': '#569CD6',       # Azul claro
            'attribute': '#9CDCFE', # Azul claro
            'selector': '#D7BA7D',  # Amarillo claro
            'property': '#9CDCFE',  # Azul claro
            'value': '#CE9178',     # Naranja claro
            
            # JSON
            'key': '#9CDCFE',       # Azul claro
            'boolean': '#569CD6',   # Azul claro
            
            # Markdown
            'heading1': '#569CD6',  # Azul claro
            'heading2': '#569CD6',  # Azul claro
            'heading3': '#569CD6',  # Azul claro
            'heading4': '#569CD6',  # Azul claro
            'bold': '#DCDCAA',      # Amarillo claro
            'italic': '#DCDCAA',    # Amarillo claro
            'link': '#CE9178',      # Naranja claro
            'code': '#D7BA7D',      # Amarillo claro
            'codeblock': '#D7BA7D', # Amarillo claro
            'quote': '#57A64A',     # Verde claro
            'list': '#DCDCAA',      # Amarillo claro
            'numlist': '#DCDCAA',   # Amarillo claro
        }
        
        if self.current_theme == 'dark':
            return dark_theme_colors.get(token_type, '#FFFFFF')
        else:
            return light_theme_colors.get(token_type, '#000000')
    
    def update_theme(self, theme):
        """
        Actualiza el tema del resaltador de sintaxis.
        
        Args:
            theme (str): Nombre del tema ('light' o 'dark')
        """
        self.current_theme = theme
        self._init_patterns()
    
    def highlight(self, text_widget, extension):
        """
        Aplica resaltado de sintaxis a un widget de texto.
        
        Args:
            text_widget (tk.Text): Widget de texto a resaltar
            extension (str): Extensión que determina el lenguaje
        """
        # Reiniciar el estado del widget
        text_widget.tag_delete(*text_widget.tag_names())
        
        # Normalizar la extensión
        extension = extension.lower()
        
        # Si no es una extensión conocida, buscar una similar
        if extension not in self.language_patterns:
            if extension in ['.jsx', '.tsx']:
                extension = '.js'
            elif extension in ['.htm', '.xhtml']:
                extension = '.html'
            elif extension in ['.scss', '.sass', '.less']:
                extension = '.css'
            elif extension in ['.yaml', '.yml']:
                extension = '.json'
            elif extension in ['.txt', '.log']:
                return  # No aplicar resaltado a archivos de texto plano
            else:
                return  # No aplicar resaltado a extensiones desconocidas
        
        # Obtener el contenido completo del widget
        content = text_widget.get("1.0", tk.END)
        
        # Obtener los patrones del lenguaje
        patterns = self.language_patterns.get(extension, [])
        
        # Crear tags para cada tipo de token
        for token_type, pattern, color in patterns:
            text_widget.tag_configure(token_type, foreground=color)
            
            # Buscar todas las coincidencias
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_index = f"1.0+{match.start()}c"
                end_index = f"1.0+{match.end()}c"
                
                # Aplicar el tag a la región
                text_widget.tag_add(token_type, start_index, end_index)
