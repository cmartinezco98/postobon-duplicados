@echo off
:: 1. Obtener la ruta de la carpeta donde está este archivo .bat
set BASE_DIR=%~dp0

:: 2. Ejecutar el script usando una ruta relativa desde el .bat
:: '..' sube un nivel, luego entra a la carpeta 'codigo'
start pythonw "%BASE_DIR%\py-modules\GUI.py"

:: Evita que la consola se cierre inmediatamente si hay un error
pause