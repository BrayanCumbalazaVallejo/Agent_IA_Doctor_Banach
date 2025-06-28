#!/bin/bash

echo "Actualizando pip..."
pip3 install --upgrade pip

echo "Instalando el proyecto y sus dependencias..."
# Esta línea ahora lee el '-e .' en requirements.txt y ejecuta setup.py
pip3 install -r requirements.txt

echo "¡Configuración completada en MacOS/Linux!"