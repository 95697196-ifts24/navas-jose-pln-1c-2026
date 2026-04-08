# Laboratorio de Introducción al PLN, LLMs y Agentic AI

**IFTS Nº 24 — Ciencia de Datos e Inteligencia Artificial**
**2do año — 1er cuatrimestre 2026**
**Prof. Matías Barreto** — Especialista en Nuevos Medios e Interactividad
matiasbarreto@ifts24.edu.ar

_Lenguaje, Algoritmos y Construcción del Presente_

---

## Qué es este repositorio

Este repositorio contiene los notebooks de laboratorio de la materia. El material se organiza en carpetas numeradas que se publican semana a semana a medida que avanza la cursada.

Cada carpeta corresponde a un bloque temático y contiene los notebooks (`.ipynb`) necesarios para trabajar en clase y fuera de ella.

---

## Requisitos previos

Antes de arrancar, asegurate de tener instalado en tu máquina:

1. **Python 3.11 o superior** — [Descarga oficial](https://www.python.org/downloads/)
   - Durante la instalación en Windows, marcá la opción **"Add Python to PATH"**.
2. **Git** — [Descarga oficial](https://git-scm.com/downloads)
3. **Visual Studio Code** (recomendado) — [Descarga oficial](https://code.visualstudio.com/)
   - Instalá la extensión **Jupyter** desde el marketplace de VS Code.
4. **FFmpeg** (requerido para notebooks de audio/video, como descargas de YouTube y transcripción con Whisper)
   - **Windows:** `winget install Gyan.FFmpeg` o `choco install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **macOS:** `brew install ffmpeg`

---

## Setup inicial (una sola vez)

Abrí una terminal (en Windows: PowerShell o Git Bash) y ejecutá los siguientes comandos:

### 1. Clonar el repositorio

```bash
git clone https://github.com/mattbarreto/ifts24-lab-pln-2026.git
cd ifts24-lab-pln-2026
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Git Bash / CMD):**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

Si PowerShell muestra un error de permisos, ejecutá primero (solo una vez en tu usuario):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Cuando el entorno esté activo, verás `(.venv)` al principio de la línea de la terminal.

### 4. Instalar las dependencias de Python

```bash
pip install -r requirements.txt
```

`requirements.txt` instala solo dependencias de Python. Si vas a trabajar con notebooks de audio/video, necesitás además `ffmpeg` y `ffprobe` a nivel sistema.

### 4.1. Instalar FFmpeg si vas a trabajar con audio/video

**Windows:**
```powershell
winget install Gyan.FFmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

Después de instalar FFmpeg, cerrá y volvé a abrir la terminal o Jupyter para que tome el nuevo `PATH`.

Si ya tenés FFmpeg instalado pero Jupyter no lo detecta, podés iniciar la sesión definiendo `FFMPEG_PATH` con la ruta completa al ejecutable.

**Windows (PowerShell):**
```powershell
$env:FFMPEG_PATH = "C:\ruta\completa\ffmpeg.exe"
jupyter lab
```

### 5. Instalar Playwright (navegadores para web scraping)

```bash
playwright install
```

### 6. Instalar componentes de Scrapling

```bash
pip scrapling install
```

### 7. Descargar recursos de NLTK

Abrí Python e ingresá:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
```

---

## Cómo actualizar cada semana

Cada vez que se publique material nuevo, desde la carpeta del repositorio ejecutá:

```bash
git pull
```

Si se agregan nuevas dependencias, se anunciará en clase. En ese caso, con el entorno activado:

```bash
pip install -r requirements.txt
```

Si el material nuevo usa audio/video, verificá además que `ffmpeg` siga disponible en tu sistema con:

```bash
ffmpeg -version
```

---

## Estructura del repositorio

```text
ifts24-lab-pln-2026/
├── README.md
├── requirements.txt
├── 001_python/
├── 002_WebScraping/
│   ├── 008_YouTube_Audio_a_Corpus.ipynb
│   └── ...
├── 003_spacy/
├── Guias/
└── ...
```

---

## Resolución de problemas frecuentes

**"python no se reconoce como comando"**
Python no se agregó al PATH durante la instalación. Reinstalá marcando "Add Python to PATH", o usá `python3` en lugar de `python`.

**"No module named 'xxx'"**
Verificá que el entorno virtual esté activado (debés ver `(.venv)` al inicio de la línea en la terminal). Si lo está, ejecutá `pip install -r requirements.txt` de nuevo.

**Error de permisos en PowerShell al activar el entorno**
Ejecutá: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Playwright no funciona / no encuentra navegador**
Ejecutá `playwright install` con el entorno activado.

**`ffmpeg` / `ffprobe` no se reconoce o aparece `FileNotFoundError` en notebooks de audio**
Instalá FFmpeg a nivel sistema (`winget install Gyan.FFmpeg`, `choco install ffmpeg`, `sudo apt install ffmpeg` o `brew install ffmpeg`) y reiniciá la terminal o Jupyter para que se actualice el `PATH`. Si ya está instalado pero el notebook no lo detecta, iniciá Jupyter con `FFMPEG_PATH` definido.

---

## Licencia

Este material se distribuye bajo licencia [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es):
podés usarlo y adaptarlo con atribución, sin fines comerciales, y compartiendo bajo la misma licencia.
