# Guía de Instalación

Esta guía detalla las diferentes formas de instalar y ejecutar el Selector de Contexto para LLMs.

## Opción 1: Ejecutable Standalone (la más sencilla)

Esta es la forma más fácil de usar la aplicación, ya que no requiere instalación de Python ni dependencias.

1. Descarga el ejecutable desde la sección de releases
   - Para Windows: `SelectorDeContexto.exe` 
   - Para macOS: `SelectorDeContexto.app`
   - Para Linux: `SelectorDeContexto`

2. Haz doble clic en el archivo descargado para iniciar la aplicación
   - En Linux, es posible que debas hacerlo ejecutable primero:
     ```bash
     chmod +x SelectorDeContexto
     ```

## Opción 2: Instalación desde el código fuente

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/directorio.git
   cd directorio
   ```

2. Instala el paquete:
   ```bash
   pip install -e .
   ```

3. Ejecuta la aplicación:
   ```bash
   context-selector
   ```
   
   Alternativamente, puedes ejecutarla directamente:
   ```bash
   python -m src.main
   ```

## Opción 3: Generar tu propio ejecutable

Si deseas distribuir la aplicación o crear un ejecutable adaptado a tu sistema:

1. Instala las dependencias de desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```

2. Ejecuta el script de construcción:
   ```bash
   python build_executable.py
   ```

3. El ejecutable generado estará disponible en la carpeta `dist/`

### Notas para la generación del ejecutable

- Para Windows: Se generará un archivo `.exe`
- Para macOS: Se generará un archivo `.app`
- Para Linux: Se generará un archivo ejecutable sin extensión

## Solución de problemas

### El ejecutable no inicia

- Windows: Asegúrate de que no sea bloqueado por el antivirus
- macOS: Es posible que debas permitir aplicaciones de desarrolladores no identificados en Preferencias del Sistema → Seguridad y Privacidad
- Linux: Verifica que el archivo tenga permisos de ejecución (`chmod +x`)

### Faltan dependencias al instalar desde el código

- Intenta instalar manualmente las dependencias:
  ```bash
  pip install tkinter
  ```
  (Nota: tkinter generalmente viene con Python, pero en algunas distribuciones de Linux puede necesitar instalarse por separado)

### PyInstaller no encuentra los recursos

- Si al generar el ejecutable faltan recursos, verifica las rutas en `build_executable.py`
- Asegúrate de que las carpetas `assets`, `config` y `resources` existan

## Soporte

Si tienes problemas durante la instalación, por favor crea un issue en el repositorio o contacta con el desarrollador.

¿Encontraste útil esta herramienta? Considera [invitarme a un café](https://buymeacoffee.com/betanzosdev) ☕
