#!/bin/bash
# Script para ejecutar directamente el Selector de Contexto para LLMs

echo "Ejecutando el Selector de Contexto para LLMs"
echo "============================================"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado."
    echo "Por favor, instala Python 3.7 o superior e intenta nuevamente."
    exit 1
fi

# Ejecutar la aplicación
python3 run.py

echo ""
echo "Presiona Enter para salir..."
read
