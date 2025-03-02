#!/bin/bash

# Script para crear una aplicación macOS (.app) para el Selector de Contexto

echo "Creando aplicación macOS para el Selector de Contexto para LLMs..."

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado."
    echo "Por favor, instala Python 3.7 o superior e intenta nuevamente."
    exit 1
fi

# Verificar que pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 no está instalado."
    echo "Por favor, instala pip e intenta nuevamente."
    exit 1
fi

# Instalar dependencias para la distribución
echo "Instalando dependencias para la distribución..."
pip3 install -r dist_requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias."
    exit 1
fi

# Generar la aplicación con PyInstaller
echo "Generando aplicación macOS..."
python3 build_executable.py
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo generar la aplicación."
    exit 1
fi

# Verificar si se generó correctamente
if [ ! -f "dist/SelectorDeContexto" ]; then
    echo "ERROR: No se encontró el ejecutable generado."
    exit 1
fi

# Crear estructura de la aplicación macOS
echo "Creando estructura de la aplicación macOS..."

# Crear carpetas necesarias
mkdir -p "dist/SelectorDeContexto.app/Contents/MacOS"
mkdir -p "dist/SelectorDeContexto.app/Contents/Resources"

# Mover el ejecutable
mv "dist/SelectorDeContexto" "dist/SelectorDeContexto.app/Contents/MacOS/"

# Copiar recursos
if [ -d "assets" ]; then
    cp -r "assets" "dist/SelectorDeContexto.app/Contents/Resources/"
fi

if [ -d "config" ]; then
    cp -r "config" "dist/SelectorDeContexto.app/Contents/Resources/"
fi

if [ -d "resources" ]; then
    cp -r "resources" "dist/SelectorDeContexto.app/Contents/Resources/"
fi

# Crear archivo Info.plist
cat > "dist/SelectorDeContexto.app/Contents/Info.plist" << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Selector de Contexto</string>
    <key>CFBundleExecutable</key>
    <string>SelectorDeContexto</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.betanzosdev.contextoselector</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>SelectorDeContexto</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOL

# Convertir .ico a .icns si está disponible
if [ -f "assets/icon.ico" ]; then
    echo "Convirtiendo icono a formato macOS..."
    
    # Crear carpeta temporal para la conversión
    mkdir -p "temp_iconset.iconset"
    
    # Convertir .ico a diferentes tamaños de .png
    # Nota: Esto requiere que sips y iconutil estén disponibles (herramientas estándar de macOS)
    sips -s format png "assets/icon.ico" --out "temp_iconset.iconset/icon_16x16.png" --resampleHeightWidth 16 16
    sips -s format png "assets/icon.ico" --out "temp_iconset.iconset/icon_32x32.png" --resampleHeightWidth 32 32
    sips -s format png "assets/icon.ico" --out "temp_iconset.iconset/icon_64x64.png" --resampleHeightWidth 64 64
    sips -s format png "assets/icon.ico" --out "temp_iconset.iconset/icon_128x128.png" --resampleHeightWidth 128 128
    sips -s format png "assets/icon.ico" --out "temp_iconset.iconset/icon_256x256.png" --resampleHeightWidth 256 256
    
    # Copiar versiones a versiones @2x
    cp "temp_iconset.iconset/icon_16x16.png" "temp_iconset.iconset/icon_16x16@2x.png"
    cp "temp_iconset.iconset/icon_32x32.png" "temp_iconset.iconset/icon_32x32@2x.png"
    cp "temp_iconset.iconset/icon_64x64.png" "temp_iconset.iconset/icon_64x64@2x.png"
    cp "temp_iconset.iconset/icon_128x128.png" "temp_iconset.iconset/icon_128x128@2x.png"
    cp "temp_iconset.iconset/icon_256x256.png" "temp_iconset.iconset/icon_256x256@2x.png"
    
    # Crear el archivo .icns
    iconutil -c icns "temp_iconset.iconset" -o "dist/SelectorDeContexto.app/Contents/Resources/icon.icns"
    
    # Limpiar archivos temporales
    rm -rf "temp_iconset.iconset"
fi

# Hacer el ejecutable ejecutable
chmod +x "dist/SelectorDeContexto.app/Contents/MacOS/SelectorDeContexto"

echo ""
echo "¡Aplicación macOS creada con éxito!"
echo "La aplicación se encuentra en: dist/SelectorDeContexto.app"
echo ""
echo "Ahora puedes arrastrarla a tu carpeta de Aplicaciones."
