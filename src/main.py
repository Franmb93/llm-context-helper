#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Selector de Contexto para LLMs.
"""

import os
import sys
from context_selector import ContextSelector

def main():
    """Función principal que inicia la aplicación."""
    app = ContextSelector()
    app.mainloop()

if __name__ == "__main__":
    main()