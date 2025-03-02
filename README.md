# Selector de Contexto para LLMs

Aplicación con interfaz gráfica para seleccionar archivos y fragmentos de código como contexto para modelos de lenguaje durante la programación.

## Descripción

Esta herramienta permite a los desarrolladores seleccionar de manera precisa fragmentos de código o archivos completos para proporcionar contexto a los modelos de lenguaje (LLMs) durante tareas de programación, mejorando significativamente las interacciones con asistentes de IA.

## Características principales

- Navegación jerárquica de directorios de código
- Visualizador de código con resaltado de sintaxis
- Selección flexible de contexto (fragmentos o archivos completos)
- Gestión y organización del contexto seleccionado
- Exportación del contexto para usar con LLMs
- Personalización y preferencias

## Instalación

### Opción 1: Instalación desde el ejecutable (recomendado)

1. Descarga el archivo ejecutable desde la sección de releases
2. Haz doble clic en el archivo descargado para iniciar la aplicación

### Opción 2: Instalación desde el código fuente

Requisitos:
- Python 3.7 o superior

```bash
# Clonar el repositorio
git clone [https://github.com/tuusuario/directorio.git](https://github.com/Franmb93/llm-context-helper.git)
cd directorio

# Instalar el paquete
pip install -e .

# Ejecutar la aplicación
context-selector
```

### Opción 3: Generar tu propio ejecutable

```bash
# Instalar las dependencias de desarrollo
pip install -e ".[dev]"

# Generar el ejecutable
python build_executable.py
```

El ejecutable generado estará disponible en la carpeta `dist/`.

## Uso

1. Abre la aplicación
2. Selecciona la carpeta que contiene tu código usando "Archivo > Abrir carpeta"
3. Navega por los archivos en el panel izquierdo
4. Haz clic en un archivo para visualizar su contenido
5. Selecciona fragmentos de código y añádelos al contexto
6. Alternativamente, marca las casillas junto a los archivos para incluirlos completos
7. Copia el contexto recopilado y pégalo en tu conversación con el LLM

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras un error o tienes una idea para mejorar la aplicación, no dudes en crear un issue o enviar un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

## Soporte

Si encuentras útil esta herramienta, considera [invitarme a un café](https://buymeacoffee.com/betanzosdev) ☕
