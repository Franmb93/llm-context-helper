# Selector de Contexto para LLMs

Aplicación con interfaz gráfica que permite seleccionar archivos y fragmentos de código como contexto para modelos de lenguaje durante la programación. Implementada en Python con Tkinter.

## Características

- **Explorador de archivos integrado:** Navegación de carpetas con filtrado por tipos de archivos de código
- **Visualizador de código:** Resaltado de sintaxis básico para lenguajes comunes
- **Selección flexible:** Añade archivos completos o fragmentos específicos al contexto
- **Funciones de exportación:** Copia el contexto al portapapeles o guárdalo en un archivo
- **Interfaces intuitivas:** Atajos de teclado y menús contextuales para operaciones comunes
- **Persistencia:** Guarda la última carpeta visitada entre sesiones

## Instalación

### Requisitos previos

- Python 3.7 o superior
- Tkinter (incluido en la instalación estándar de Python)

### Instalación desde el código fuente

1. Clona el repositorio:
   ```
   git clone https://github.com/yourusername/context-selector.git
   cd context-selector
   ```

2. Instala el paquete en modo de desarrollo:
   ```
   pip install -e .
   ```

3. Ejecuta la aplicación:
   ```
   context-selector
   ```

O simplemente puedes ejecutar el script principal:
```
python src/main.py
```

## Uso

1. **Seleccionar carpeta:** Inicia seleccionando una carpeta de proyecto con el botón "Seleccionar carpeta" o mediante Archivo -> Abrir carpeta
2. **Navegar archivos:** Explora la estructura de archivos en el panel izquierdo
3. **Ver contenido:** Haz clic en un archivo para mostrar su contenido en el panel central
4. **Añadir al contexto:** Selecciona fragmentos de código y haz clic en "Añadir selección al contexto" o usa el menú contextual
5. **Gestionar contexto:** Revisa las selecciones en el panel inferior, elimínalas si es necesario
6. **Exportar:** Copia el contexto completo al portapapeles o guárdalo en un archivo

### Atajos de teclado

- **Ctrl+O:** Abrir carpeta
- **Ctrl+S:** Guardar contexto
- **Ctrl+A:** Añadir selección al contexto
- **Ctrl+L:** Limpiar contexto
- **Ctrl+C:** Copiar selección actual (en el visor de código)

## Estructura del proyecto

```
context_selector/
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada principal
│   ├── context_selector.py  # Clase principal de la aplicación
│   ├── file_manager.py      # Gestión de archivos y carpetas
│   ├── syntax_highlighter.py # Resaltado de sintaxis básico
│   └── utils.py             # Funciones auxiliares
│
├── resources/
│   └── icons/               # Iconos para la interfaz
│
├── config/
│   └── settings.json        # Configuración de la aplicación
│
├── README.md                # Documentación
├── requirements.txt         # Dependencias
└── setup.py                 # Configuración de instalación
```

## Personalización

La aplicación guarda la configuración en el archivo `config/settings.json`. Actualmente almacena:

- La última carpeta visitada (para restaurarla en la próxima sesión)

En futuras versiones se añadirán más opciones de configuración como temas, tamaños de fuente, y extensiones de archivo a filtrar.

## Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, por favor abre primero un issue para discutir qué te gustaría cambiar.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).