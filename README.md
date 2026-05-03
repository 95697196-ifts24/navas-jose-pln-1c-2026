# navas-jose-pln-1c-2026

Repositorio de trabajo para la materia de Procesamiento de Lenguaje Natural, LLMs y Agentic AI del IFTS Nro. 24, primer cuatrimestre 2026.

El proyecto contiene notebooks de clase, trabajos practicos integradores, corpus de analisis y dashboards de apoyo para estudiar tecnicas de PLN aplicadas a textos periodisticos, scraping, spaCy, vectorizacion, text mining y representaciones semanticas.

## Repositorio

```bash
git clone https://github.com/95697196-ifts24/navas-jose-pln-1c-2026.git
cd navas-jose-pln-1c-2026
```

Si el remoto local apunta a otro repositorio, corregirlo con:

```bash
git remote set-url origin https://github.com/95697196-ifts24/navas-jose-pln-1c-2026.git
git remote -v
```

## Requisitos

- Python 3.11 o superior.
- Git.
- Visual Studio Code con extension Jupyter.
- FFmpeg para notebooks de audio, video o Whisper.
- Navegadores de Playwright para notebooks de scraping dinamico.

En Windows, FFmpeg puede instalarse con:

```powershell
winget install Gyan.FFmpeg
```

## Instalacion

### Opcion recomendada

```bash
python -m venv .venv
```

Activar el entorno:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
playwright install
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

Para notebooks de audio:

```bash
pip install -r requirements-audio.txt
```

### Scripts incluidos

En Windows:

```powershell
.\setup.ps1
```

En macOS o Linux:

```bash
./setup.sh
```

## Estructura del proyecto

```text
navas-jose-pln-1c-2026/
├── 001_python/                         # Fundamentos de Python para PLN
├── 002_adquisicion_corpus/             # Requests, scraping, Trafilatura, Playwright, audio
├── 003_spacy/                          # Pipeline spaCy, tokens, lemas, POS, NER, Matcher
├── 004_tpi_1/                          # Trabajo practico integrador 1
├── 005_Vectorizacion/                  # Bag of Words, TF-IDF y n-gramas
├── 006_lab_integrador_guiado/          # Laboratorio integrador guiado
├── 007_tpi_2/                          # Trabajo practico integrador 2
├── 007_tpi_3/                          # TP3 recuperatorio y corpus de trabajo
├── 008_representaciones_semanticas/    # Coocurrencias, embeddings y semantica
├── 009_tpi3_text_mining_recuperatorio/ # Version de trabajo del TP3 text mining
├── Extras/                             # Dashboards HTML de apoyo
├── Guias/                              # Guias complementarias
├── requirements.txt
├── requirements-audio.txt
└── README.md
```

## TP3 recuperatorio

La carpeta `007_tpi_3/` contiene los materiales principales para el TP3:

- `TP3_Recuperatorio_Grupal1.ipynb`
- `TP3_Recuperatorio_Grupal2.ipynb`
- `corpus_tp3.csv`
- `TP3.pptx`

El trabajo se centra en un corpus comparativo de 12 textos sobre inteligencia artificial:

- 6 textos del grupo `mit`
- 6 textos del grupo `bbc`

Tecnicas principales utilizadas:

- validacion y auditoria del corpus;
- normalizacion de columnas y fechas;
- procesamiento con spaCy;
- tokenizacion, lematizacion, POS, dependencias y rasgos morfologicos;
- reconocimiento de entidades nombradas;
- comparacion de stopwords de spaCy y NLTK;
- ajustes humanos del pipeline con stopwords propias, correcciones de lemas, `Matcher` y `EntityRuler`;
- Bag of Words;
- TF-IDF;
- bigramas;
- visualizaciones con Matplotlib y Seaborn;
- vuelta a fragmentos concretos para lectura cercana.

## Dashboards

La carpeta `Extras/` incluye dashboards HTML que se pueden abrir directamente en el navegador:

- `dashboard_tecnicas_pln.html`: resumen general de tecnicas de PLN.
- `dashboard_tecnicas_tp_3.html`: guia especifica para resolver y analizar el TP3 recuperatorio.

Para abrirlos no hace falta levantar servidor. Se pueden abrir con doble clic o desde el navegador.

## Flujo de trabajo con Git

Ver estado:

```bash
git status
```

Agregar cambios:

```bash
git add .
```

Crear commit:

```bash
git commit -m "Actualiza avance del proyecto PLN"
```

Subir a GitHub:

```bash
git push origin main
```

Si la rama principal se llama `master`:

```bash
git push origin master
```

## Problemas frecuentes

### El entorno virtual no activa en PowerShell

Ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego activar:

```powershell
.venv\Scripts\Activate.ps1
```

### Falta un paquete

Con el entorno activado:

```bash
pip install -r requirements.txt
```

### Falta el modelo de spaCy

Para el TP3 se usa normalmente el modelo mediano de espanol:

```bash
python -m spacy download es_core_news_md
```

### Playwright no encuentra navegador

```bash
playwright install
```

### GitHub devuelve error 403 al hacer push

Verificar que `origin` apunte al repositorio correcto:

```bash
git remote -v
git remote set-url origin https://github.com/95697196-ifts24/navas-jose-pln-1c-2026.git
```

## Nota academica

Los notebooks y dashboards estan pensados como material de aprendizaje. Las tecnicas automaticas de PLN ayudan a detectar patrones, pero las conclusiones deben justificarse con decisiones metodologicas claras, visualizaciones legibles y lectura de fragmentos concretos del corpus.

## Licencia

Material academico para uso educativo. Si se reutiliza o adapta, citar la fuente original de la cursada y mantener el uso no comercial.
