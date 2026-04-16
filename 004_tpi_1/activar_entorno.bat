@echo off
:: Script de activación del entorno virtual del TPI 1
:: Doble-click en este archivo para abrir una terminal ya configurada

echo ============================================
echo  TPI 1 - Entorno Virtual PLN 2026
echo ============================================
echo.

:: Activamos el entorno virtual
call "%~dp0.venv\Scripts\activate.bat"

echo  Python: && python --version
echo  FFmpeg: && ffmpeg -version 2>&1 | findstr "version"
echo.
echo  Para ejecutar el proyecto:
echo    python TPI_1_solucion.py
echo.

:: Abrimos una consola interactiva en la carpeta del proyecto
cmd /k "cd /d %~dp0"
