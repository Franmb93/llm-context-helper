# Scripts de Instalación del Selector de Contexto

Esta carpeta contiene los scripts necesarios para instalar, empaquetar y distribuir la aplicación Selector de Contexto para LLMs.

## Scripts Principales

### Para Usuarios Finales

- **`install.bat`** - Script de instalación universal para Windows (recomendado)
- **`install.sh`** - Script de instalación para sistemas Linux/macOS

### Para Desarrolladores

- **`installer.py`** - Instalador Python completo (multiplataforma)
- **`fix_imports.py`** - Corrige las importaciones relativas en el código
- **`build_standalone.py`** - Script para construir el ejecutable

## Generación de Ejecutables

Para generar un ejecutable standalone de la aplicación:

### En Windows:
```
install.bat
```

### En Linux/macOS:
```
./install.sh
```

### Opciones avanzadas:
```
python installers/installer.py
```

## Detalles Técnicos

Los instaladores realizan las siguientes operaciones:

1. Verificación de requisitos del sistema (Python, Tkinter)
2. Instalación de dependencias necesarias (PyInstaller)
3. Corrección automática de importaciones relativas
4. Creación de un bootstrapper para el entorno de ejecución
5. Empaquetado de la aplicación con todos los recursos

## Notas sobre Distribución

El ejecutable generado se encuentra en la carpeta `dist/` y puede distribuirse directamente a usuarios finales. No requiere una instalación previa de Python.
