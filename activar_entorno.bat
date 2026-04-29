@echo off
:: Script de activacion del entorno PLN - IFTS 24
:: Ejecutar con doble click o desde la terminal: activar_entorno.bat

echo ============================================
echo  Laboratorio PLN - IFTS N. 24 - 2026
echo ============================================

if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: El entorno virtual no existe.
    echo Ejecuta setup.ps1 primero desde PowerShell.
    pause
    exit /b 1
)

echo Activando entorno virtual ^(Python 3.11^)...
call .venv\Scripts\activate.bat

echo Entorno activado correctamente.
echo Python: && python --version
echo Jupyter disponible: && jupyter --version 2>nul | findstr /i "lab"
echo.
echo Para iniciar JupyterLab ejecuta:
echo   jupyter lab
echo.
echo Para desactivar el entorno ejecuta:
echo   deactivate
echo.
