#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador universal para el Selector de Contexto para LLMs.
Este script funciona en Windows, macOS y Linux, y se encarga de:
1. Verificar requisitos
2. Crear carpetas necesarias
3. Generar un ejecutable independiente
"""

import os
import sys
import shutil
import subprocess
import platform
import tempfile
import importlib.util

# Definir colores para la consola si es compatible
if platform.system() != "Windows" or "ANSICON" in os.environ:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
else:
    RESET = GREEN = RED = YELLOW = BLUE = BOLD = ""

def print_header(text):
    """Imprime un encabezado formateado."""
    print(f"\n{BOLD}{BLUE}=== {text} ==={RESET}\n")

def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Imprime un mensaje de error."""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    """Imprime un mensaje de advertencia."""
    print(f"{YELLOW}! {text}{RESET}")

def print_info(text):
    """Imprime un mensaje informativo."""
    print(f"  {text}")

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    print_header("Verificando versión de Python")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python {version_str} detectado (compatible)")
        return True
    else:
        print_error(f"Python {version_str} detectado (incompatible)")
        print_info("Se requiere Python 3.7 o superior")
        return False

def check_tkinter():
    """Verifica que Tkinter esté instalado."""
    print_header("Verificando Tkinter")
    
    try:
        import tkinter
        version = tkinter.TkVersion
        print_success(f"Tkinter {version} detectado")
        return True
    except ImportError:
        print_error("Tkinter no está instalado")
        if platform.system() == "Linux":
            print_info("Instálalo con uno de estos comandos:")
            print_info("  Ubuntu/Debian: sudo apt install python3-tk")
            print_info("  Fedora: sudo dnf install python3-tkinter")
            print_info("  Arch: sudo pacman -S tk")
        elif platform.system() == "Darwin":  # macOS
            print_info("Instálalo con: brew install python-tk")
        return False

def check_and_install_pyinstaller():
    """Verifica que PyInstaller esté instalado y lo instala si es necesario."""
    print_header("Verificando PyInstaller")
    
    pyinstaller_spec = importlib.util.find_spec("PyInstaller")
    
    if pyinstaller_spec:
        try:
            import PyInstaller
            print_success(f"PyInstaller {PyInstaller.__version__} ya está instalado")
            return True
        except (ImportError, AttributeError):
            print_warning("PyInstaller está instalado pero no se puede determinar la versión")
            return True
    
    print_info("PyInstaller no está instalado. Instalando...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True)
        print_success("PyInstaller instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al instalar PyInstaller: {e}")
        print_info(f"Detalles: {e.stderr.decode() if e.stderr else 'No hay detalles disponibles'}")
        return False

def create_bootstrap_file():
    """Crea un archivo temporal con el código bootstrap para PyInstaller."""
    print_header("Creando archivo de arranque")
    
    temp_dir = tempfile.mkdtemp()
    bootstrap_path = os.path.join(temp_dir, "context_selector_bootstrap.py")
    
    with open(bootstrap_path, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de arranque para el Selector de Contexto con soporte para ejecución en modo frozen.
"""

import os
import sys

# Ajustar el path para importaciones ya sea en modo desarrollo o congelado
if getattr(sys, 'frozen', False):
    # Se está ejecutando desde un bundle congelado
    bundle_dir = os.path.dirname(sys.executable)
    # Añadir todas las rutas necesarias para el modo congelado
    sys.path.insert(0, bundle_dir)
else:
    # Se está ejecutando en modo de desarrollo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(script_dir, '..')))

# Importar la aplicación principal
from src.core.app import ContextSelectorApp

def fix_imports(project_dir):
    """Corrige las importaciones relativas en todos los archivos del proyecto."""
    print_header("Corrigiendo importaciones relativas")
    
    script_path = os.path.join(project_dir, "fix_imports.py")
    if not os.path.exists(script_path):
        print_error("No se encuentra el script fix_imports.py")
        return False
    
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print_success("Importaciones corregidas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al corregir importaciones: {e}")
        return False

def main():
    """Iniciar la aplicación."""
    app = ContextSelectorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
''')
    
    print_success(f"Archivo de arranque creado en: {bootstrap_path}")
    return temp_dir, bootstrap_path

def verify_project_directories(project_dir):
    """Verifica que los directorios del proyecto existan."""
    print_header("Verificando directorios del proyecto")
    
    directories = ["assets", "config", "resources", "src"]
    all_present = True
    
    for directory in directories:
        dir_path = os.path.join(project_dir, directory)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print_success(f"Directorio {directory} encontrado")
        else:
            print_error(f"Directorio {directory} no encontrado en {dir_path}")
            all_present = False
    
    if not all_present:
        print_warning("Faltan algunos directorios requeridos")
        print_info("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
    
    return all_present

def build_executable(project_dir, bootstrap_path):
    """Construye el ejecutable usando PyInstaller."""
    print_header("Generando ejecutable")
    
    # Definir rutas absolutas para los recursos
    assets_dir = os.path.join(project_dir, "assets")
    config_dir = os.path.join(project_dir, "config")
    resources_dir = os.path.join(project_dir, "resources")
    src_dir = os.path.join(project_dir, "src")
    
    # Determinar el separador de path según el sistema operativo
    path_sep = ";" if platform.system() == "Windows" else ":"
    
    # Nombre del ejecutable según el sistema operativo
    exe_name = "SelectorDeContexto"
    if platform.system() == "Windows":
        exe_name += ".exe"
    
    # Ubicación del icono
    icon_option = []
    icon_path = os.path.join(assets_dir, "icon.ico")
    if os.path.exists(icon_path):
        icon_option = [f"--icon={icon_path}"]
    
    # Directorio de salida
    output_dir = os.path.join(project_dir, "dist")
    
    # Crear lista de argumentos para PyInstaller
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--name=" + exe_name,
        "--onefile",
        "--windowed",
        "--clean",
        "--distpath=" + output_dir,
        "--workpath=" + os.path.join(project_dir, "build"),
        "--specpath=" + os.path.join(project_dir, "build"),
        bootstrap_path,
        f"--add-data={assets_dir}{path_sep}assets",
        f"--add-data={config_dir}{path_sep}config",
        f"--add-data={resources_dir}{path_sep}resources",
        f"--add-data={src_dir}{path_sep}src"
    ]
    
    # Añadir icono si existe
    if icon_option:
        pyinstaller_args.extend(icon_option)
    
    # Ejecutar PyInstaller
    print_info("Ejecutando PyInstaller...")
    
    try:
        process = subprocess.Popen(
            pyinstaller_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Mostrar la salida en tiempo real
        for line in process.stdout:
            line = line.strip()
            if "INFO:" in line:
                print_info(line)
            elif "WARNING:" in line:
                print_warning(line)
            elif "ERROR:" in line:
                print_error(line)
            else:
                print(line)
        
        process.wait()
        
        if process.returncode == 0:
            exe_path = os.path.join(output_dir, exe_name)
            print_success(f"Ejecutable generado correctamente en: {exe_path}")
            return True, exe_path
        else:
            print_error(f"Error al generar el ejecutable (código {process.returncode})")
            return False, None
    
    except Exception as e:
        print_error(f"Error durante la generación del ejecutable: {str(e)}")
        return False, None

def create_shortcut(exe_path):
    """Crea un acceso directo al ejecutable."""
    if platform.system() != "Windows":
        print_info("La creación de accesos directos solo está soportada en Windows")
        return False
    
    print_header("Creando acceso directo")
    
    try:
        import ctypes.wintypes
        CSIDL_DESKTOP = 0x0000
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOP, 0, 0, buf)
        desktop_path = buf.value
        
        shortcut_path = os.path.join(desktop_path, "Selector de Contexto para LLMs.lnk")
        
        # Usar PowerShell para crear el acceso directo
        ps_command = f'''
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = '{exe_path}'
        $Shortcut.Description = 'Selector de Contexto para LLMs'
        $Shortcut.WorkingDirectory = '{os.path.dirname(exe_path)}'
        '''
        
        # Añadir icono si existe
        icon_path = os.path.join(os.path.dirname(os.path.dirname(exe_path)), "assets", "icon.ico")
        if os.path.exists(icon_path):
            ps_command += f'''
            $Shortcut.IconLocation = '{icon_path}'
            '''
        
        ps_command += '''
        $Shortcut.Save()
        '''
        
        # Ejecutar el comando de PowerShell
        subprocess.run(["powershell", "-Command", ps_command], check=True)
        
        print_success(f"Acceso directo creado en: {shortcut_path}")
        return True
    
    except Exception as e:
        print_error(f"Error al crear el acceso directo: {str(e)}")
        return False

def cleanup(temp_dir):
    """Limpia archivos temporales."""
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print_info("Archivos temporales eliminados")
    except Exception as e:
        print_warning(f"No se pudieron eliminar todos los archivos temporales: {str(e)}")

def main():
    """Función principal del instalador."""
    print(f"{BOLD}{YELLOW}Instalador del Selector de Contexto para LLMs{RESET}")
    print(f"{BOLD}{YELLOW}=========================================={RESET}\n")
    
    # Obtener la ruta del directorio del proyecto
    project_dir = os.path.abspath(os.path.dirname(__file__))
    print_info(f"Directorio del proyecto: {project_dir}")
    
    # Verificar requisitos
    if not check_python_version() or not check_tkinter():
        return 1
    
    if not check_and_install_pyinstaller():
        return 1
    
    if not verify_project_directories(project_dir):
        response = input("\n¿Continuar de todos modos? (s/n): ").strip().lower()
        if response != 's' and response != 'si' and response != 'sí' and response != 'y' and response != 'yes':
            print_info("Instalación cancelada")
            return 1
    
    # Corregir importaciones relativas primero
    fix_imports(project_dir)
    
    # Crear archivo bootstrap
    temp_dir, bootstrap_path = create_bootstrap_file()
    
    try:
        # Construir el ejecutable
        success, exe_path = build_executable(project_dir, bootstrap_path)
        
        if not success:
            return 1
        
        # Crear acceso directo si es Windows
        if platform.system() == "Windows":
            response = input("\n¿Crear un acceso directo en el escritorio? (s/n): ").strip().lower()
            if response == 's' or response == 'si' or response == 'sí' or response == 'y' or response == 'yes':
                create_shortcut(exe_path)
        
        print(f"\n{BOLD}{GREEN}¡Instalación completada con éxito!{RESET}")
        print_info(f"El ejecutable se encuentra en: {exe_path}")
        print_info("Para cualquier problema o sugerencia, visita: https://buymeacoffee.com/betanzosdev")
        
        return 0
    
    finally:
        # Limpiar archivos temporales
        cleanup(temp_dir)

if __name__ == "__main__":
    sys.exit(main())
