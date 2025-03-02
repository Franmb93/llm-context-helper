#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para la instalación del paquete Selector de Contexto para LLMs.
"""

from setuptools import setup, find_packages

setup(
    name="context-selector",
    version="1.0.0",
    description="Aplicación para seleccionar archivos y fragmentos de código como contexto para modelos de lenguaje",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        # Sin dependencias externas principales, solo usa tkinter que viene con Python
    ],
    extras_require={
        "dev": [
            "pyinstaller>=5.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Desktop Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "context-selector=src.main:main",
        ],
    },
    keywords="llm, ai, context, code, development",
)