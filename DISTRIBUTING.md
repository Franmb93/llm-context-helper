# Guía de Distribución

Esta guía proporciona instrucciones para distribuir el Selector de Contexto para LLMs en diferentes plataformas.

## Generando ejecutables para distribución

El proyecto incluye scripts para facilitar la creación de ejecutables en diferentes plataformas.

### En Windows

1. Ejecuta el script de creación de instalador:
   ```
   create_windows_installer.bat
   ```
   
   Este script:
   - Verifica que Python esté instalado
   - Instala las dependencias necesarias
   - Genera el ejecutable con PyInstaller
   - Opcionalmente crea un acceso directo en el escritorio

2. El ejecutable resultante estará en la carpeta `dist/`

### En macOS

1. Haz ejecutable el script de creación:
   ```bash
   chmod +x create_macos_app.sh
   ```

2. Ejecuta el script:
   ```bash
   ./create_macos_app.sh
   ```
   
   Este script:
   - Crea una estructura de aplicación macOS (.app)
   - Configura los recursos necesarios
   - Genera un archivo Info.plist
   - Convierte el icono al formato .icns si es posible

3. La aplicación resultante estará en la carpeta `dist/`

### En Linux

1. Utiliza el script general de Python:
   ```bash
   python3 build_executable.py
   ```

2. El ejecutable resultante estará en la carpeta `dist/`

## Distribución a usuarios finales

### Opciones para Windows

1. **Carpeta simple**:
   - Comprime la carpeta `dist/` en un archivo ZIP
   - Los usuarios pueden extraer y ejecutar directamente

2. **Instalador avanzado** (opcional):
   - Utiliza herramientas como NSIS o Inno Setup para crear un instalador más profesional
   - Ejemplo con Inno Setup en `create_inno_installer.iss`

### Opciones para macOS

1. **Distribución directa**:
   - Comprime `dist/SelectorDeContexto.app` en un archivo ZIP
   - Los usuarios pueden extraer y arrastrar a su carpeta de Aplicaciones

2. **Creación de DMG** (opcional):
   - Usa `create-dmg` para crear un archivo DMG más profesional
   - Referencia: https://github.com/create-dmg/create-dmg

### Opciones para Linux

1. **Distribución como AppImage**:
   - Convierte el ejecutable en un AppImage
   - Funciona en la mayoría de distribuciones sin instalación

2. **Paquetes específicos** (opcional):
   - `.deb` para Ubuntu/Debian
   - `.rpm` para Fedora/RHEL
   - Instrucciones detalladas en `linux_packaging.md`

## Consejos para una distribución efectiva

1. **Actualizaciones**:
   - Considera implementar un mecanismo de verificación de actualizaciones
   - Puede ser tan simple como comprobar una versión en un archivo JSON online

2. **Documentación**:
   - Incluye los archivos README.md e INSTALL.md con la distribución
   - Proporciona ejemplos de uso y casos comunes

3. **Soporte**:
   - Incluye información de contacto o enlace a repositorio para reportar problemas
   - Considera incluir un archivo FAQ con problemas comunes

4. **Licencia**:
   - Asegúrate de incluir el archivo de licencia con la distribución

## Consideraciones legales y de seguridad

1. **Distribución multiplataforma**:
   - Los ejecutables pueden ser bloqueados por antivirus o firewalls
   - Considera firmar digitalmente tus ejecutables para mayor confianza

2. **Privacidad**:
   - Incluye una política de privacidad si la aplicación recolecta cualquier dato
   - El Selector de Contexto no debería recolectar datos por defecto

3. **Open Source**:
   - Si distribuyes bajo licencia MIT, asegúrate de incluir el archivo LICENSE

4. **Donaciones**:
   - El botón "Buy me a coffee!" está incluido en la interfaz
   - Considera mencionar esta opción en la documentación

## Apoyo adicional

Si encuentras útil esta herramienta o necesitas soporte personalizado, considera [invitarme a un café](https://buymeacoffee.com/betanzosdev) ☕
