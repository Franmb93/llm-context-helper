@echo off
echo Instalador simple para el Selector de Contexto para LLMs
echo =======================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no está instalado o no está en el PATH.
    echo Por favor, instala Python 3.7 o superior e intenta nuevamente.
    pause
    exit /b 1
)

REM Verificar que pip está instalado
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip no está instalado o no está en el PATH.
    echo Por favor, instala pip e intenta nuevamente.
    pause
    exit /b 1
)

REM Instalar PyInstaller directamente
echo Instalando PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo instalar PyInstaller.
    pause
    exit /b 1
)

REM Construir el ejecutable directamente sin usar build_executable.py
echo Generando ejecutable con PyInstaller...
python -m PyInstaller --name=SelectorDeContexto --onefile --windowed --clean --icon=assets\icon.ico src/main.py --add-data assets;assets --add-data config;config --add-data resources;resources
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo generar el ejecutable.
    pause
    exit /b 1
)

REM Crear un acceso directo en el escritorio (opcional)
echo ¿Deseas crear un acceso directo en el escritorio? (S/N)
set /p crear_acceso=

if /i "%crear_acceso%"=="S" (
    echo Creando acceso directo en el escritorio...
    
    REM Ubicación del ejecutable generado
    set "exe_path=%CD%\dist\SelectorDeContexto.exe"
    
    REM Ubicación del icono
    set "icon_path=%CD%\assets\icon.ico"
    
    REM Escritorio del usuario
    set "desktop=%USERPROFILE%\Desktop"
    
    REM Crear acceso directo usando PowerShell
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\Selector de Contexto para LLMs.lnk'); $Shortcut.TargetPath = '%exe_path%'; if (Test-Path '%icon_path%') { $Shortcut.IconLocation = '%icon_path%' }; $Shortcut.Description = 'Selector de Contexto para LLMs'; $Shortcut.Save()"
    
    echo Acceso directo creado en el escritorio.
)

echo.
echo ¡Instalación completada con éxito!
echo El ejecutable se encuentra en la carpeta "dist".
echo.
echo Presiona cualquier tecla para salir...
pause >nul
