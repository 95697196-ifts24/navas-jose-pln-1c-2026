# ============================================================
# Script de configuracion inicial para Windows (PowerShell)
# Laboratorio de PLN - IFTS N. 24 - 2026
# Uso: powershell -ExecutionPolicy Bypass -File setup.ps1
# ============================================================

$PythonExe = "$env:USERPROFILE\.local\bin\python3.11.exe"
$VenvPath = ".venv"
$Pip = "$VenvPath\Scripts\pip.exe"
$Python = "$VenvPath\Scripts\python.exe"

Write-Host "Iniciando configuracion del entorno PLN..." -ForegroundColor Cyan

# --- Verificar Python 3.11 ---
if (-not (Test-Path $PythonExe)) {
    Write-Host "ERROR: Python 3.11 no encontrado en $PythonExe" -ForegroundColor Red
    Write-Host "Instalar con: winget install Astral-sh.uv" -ForegroundColor Yellow
    Write-Host "Luego: uv python install 3.11" -ForegroundColor Yellow
    exit 1
}

# --- Crear entorno virtual ---
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creando entorno virtual con Python 3.11..." -ForegroundColor Yellow
    & $PythonExe -m venv $VenvPath
} else {
    Write-Host "El entorno virtual ya existe." -ForegroundColor Green
}

# --- Actualizar pip ---
Write-Host "Actualizando pip..." -ForegroundColor Yellow
& $Python -m pip install --upgrade pip --quiet

# --- Instalar dependencias core ---
Write-Host "Instalando paquetes core de PLN..." -ForegroundColor Yellow
& $Pip install -r requirements.txt

# --- Instalar navegadores Playwright ---
Write-Host "Instalando navegadores para Web Scraping..." -ForegroundColor Yellow
& $VenvPath\Scripts\playwright.exe install chromium

# --- Descargar recursos NLTK ---
Write-Host "Descargando recursos NLTK..." -ForegroundColor Yellow
& $Python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')"

# --- Descargar modelos spaCy ---
Write-Host "Descargando modelos spaCy en espanol..." -ForegroundColor Yellow
& $Python -m spacy download es_core_news_sm
& $Python -m spacy download es_core_news_md

Write-Host ""
Write-Host "Configuracion completada." -ForegroundColor Green
Write-Host "Para activar el entorno: .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "Para JupyterLab: jupyter lab" -ForegroundColor Gray
Write-Host ""
Write-Host "Para instalar soporte de audio (Whisper/Torch):" -ForegroundColor Yellow
Write-Host "  pip install -r requirements-audio.txt" -ForegroundColor Yellow
