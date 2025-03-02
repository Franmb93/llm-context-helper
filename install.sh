#!/bin/bash
# Instalador para Linux/macOS del Selector de Contexto para LLMs

echo "Instalador del Selector de Contexto para LLMs"
echo "============================================="
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado."
    echo "Por favor, instala Python 3.7 o superior e intenta nuevamente."
    exit 1
fi

# Ejecutar el instalador universal
python3 installers/installer.py

echo ""
echo "Presiona Enter para salir..."
read
