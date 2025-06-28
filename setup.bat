@echo off

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando el proyecto y sus dependencias...
rem Este comando ahora lee el '-e .' en requirements.txt y ejecuta setup.py
pip install -r requirements.txt

echo ¡Configuracion completada en Windows!
pause