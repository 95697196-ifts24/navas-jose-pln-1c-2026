# Notebook "De Audio a Texto — Extracción de Corpus desde Fuentes Audiovisuales"

## CONTEXTO GENERAL

Sos el agente encargado de generar un Jupyter Notebook (.ipynb) para un curso de **Procesamiento del Lenguaje Natural y LLMs** del IFTS N.° 24 (Buenos Aires), programa de Ciencia de Datos e Inteligencia Artificial, segundo/tercer año.

**Ubicación curricular:** Este notebook cierra el **Bloque 1: Adquisición de Corpus**. Los estudiantes ya trabajaron webscraping (Trafilatura, BeautifulSoup4, Playwright, Scrapling). Ahora completan el repertorio de fuentes incorporando **texto extraído de audio**. Después de este lab pasan a spaCy y text mining.

**Hipótesis vertebradora del curso:** "Los LLMs son menos una ruptura con la lingüística que su realización técnica bajo condiciones estadísticas."

**Nivel de los estudiantes:** Saben Python intermedio, ya usaron pip, ya trabajaron con notebooks. No asumas que tienen GPU.

**Tono:** Usá la skill de estilo rioplatense académico adjunta. Español rioplatense, registro académico pero amigable, sin emojis. Pretérito perfecto simple para acciones completadas.

---

## ESTRUCTURA DEL NOTEBOOK — CELDA POR CELDA

### CELDA 1 — Markdown: Portada y metadatos
```
# De Audio a Texto — Extracción de Corpus desde Fuentes Audiovisuales
## PLN LAB · IFTS N.° 24 · Ciencia de Datos e Inteligencia Artificial
### Bloque 1: Adquisición de Corpus — Clase [N]

**Objetivo:** Incorporar fuentes audiovisuales al repertorio de adquisición de corpus textual, completando el pipeline webscraping → transcripción → texto procesable.

**Herramientas principales:** `yt-dlp`, `openai-whisper` / `faster-whisper`
**Tiempo estimado:** 2 horas de laboratorio
```

---

### CELDA 2 — Markdown: Encuadre conceptual — ¿Por qué extraer texto de audio?
Desarrollar los siguientes puntos en prosa (NO listas):
- En la práctica profesional de PLN, una proporción significativa de los corpus proviene de fuentes orales: entrevistas, podcasts, conferencias, sesiones legislativas, testimonios.
- Un pipeline de NLP que solo contempla texto escrito de la web tiene un punto ciego importante.
- La transcripción automática (ASR — Automatic Speech Recognition) es hoy un problema técnicamente resuelto gracias a modelos como Whisper.
- Encuadre epistemológico breve: la conversión audio→texto no es neutra; implica decisiones sobre puntuación, segmentación, identificación de hablantes, manejo de hesitaciones y ruido. Estas decisiones afectan el análisis lingüístico posterior.

---

### CELDA 3 — Markdown: Panorama de fuentes audiovisuales
Título: "Más allá de YouTube: un mapa de fuentes de audio transcribibles"

Organizar en una **tabla Markdown** con tres columnas: Tipo de fuente | Ejemplos concretos | Método de obtención.

Incluir al menos estas categorías:
1. **Plataformas de video:** YouTube, Vimeo, Twitch, TikTok, Instagram Reels, Facebook Video. Método: `yt-dlp`.
2. **Podcasts y audio:** Spotify, iVoox, SoundCloud, feeds RSS con .mp3 directo. Método: `yt-dlp`, `spotdl`, descarga directa.
3. **Repositorios institucionales:** Archivos orales de bibliotecas nacionales, archivos universitarios, proyectos de historia oral (ej: StoryCorps, Archivo de la Palabra). Método: descarga directa o scraping.
4. **Medios de comunicación:** Radios online con archivo, sesiones legislativas transmitidas, conferencias de prensa. Método: `yt-dlp` o descarga directa.
5. **Conferencias y educación:** Charlas TED, grabaciones de Zoom/Meet/Teams, MOOCs. Método: APIs específicas, exportación, `yt-dlp`.
6. **Mensajería:** Audios de WhatsApp (.opus), Telegram, Signal. Método: exportación manual del chat.
7. **Fuentes de campo propias:** Entrevistas grabadas, registros etnográficos, testimonios orales. Método: grabación directa.

Después de la tabla, un párrafo breve que destaque: **la herramienta de transcripción (Whisper) es siempre la misma; lo que varía es el método de obtención del audio.** Eso unifica el pipeline.

---

### CELDA 4 — Markdown: Consideraciones éticas y legales
Párrafo breve pero firme sobre:
- Derechos de autor y términos de servicio de las plataformas.
- Diferencia entre uso con fines educativos/investigativos y distribución comercial.
- Consentimiento informado cuando se trabaja con testimonios orales o entrevistas.
- La transcripción como dato sensible: los audios pueden contener información personal identificable.
- Recomendación: trabajar con contenido de licencia abierta (Creative Commons) o con consentimiento explícito para actividades del curso.

---

### CELDA 5 — Markdown: Sección práctica — Setup del entorno
Título: "Preparación del entorno de trabajo"

Breve explicación de las dos herramientas principales:
- **`yt-dlp`**: fork mantenido de youtube-dl, soporta cientos de sitios, extrae audio en múltiples formatos.
- **`openai-whisper`**: modelo de ASR de OpenAI, open-source, corre local, excelente en español. Alternativa liviana: `faster-whisper`.
- **`ffmpeg`**: dependencia necesaria para conversión de formatos de audio.

---

### CELDA 6 — Código: Instalación de dependencias
```python
# Instalación de dependencias
# NOTA: ejecutar una sola vez. Si ya están instaladas, saltar esta celda.

!pip install yt-dlp
!pip install openai-whisper   # Alternativa liviana: pip install faster-whisper
!pip install ffmpeg-python

# Verificar que ffmpeg esté disponible en el sistema
!ffmpeg -version | head -1
```
Agregar una nota en comentario: si ffmpeg no está instalado a nivel sistema, indicar cómo instalarlo según OS (apt, brew, choco).

---

### CELDA 7 — Markdown: Paso 1 — Descarga de audio desde YouTube
Explicar brevemente:
- `yt-dlp` permite descargar solo la pista de audio (sin video) con la flag `--extract-audio`.
- Se puede elegir formato (mp3, wav, opus) y calidad.
- Mostrar la URL de ejemplo: usar un video de **dominio público o Creative Commons** (sugerir un video de una conferencia académica o charla TED con licencia abierta).

---

### CELDA 8 — Código: Descarga de audio con yt-dlp
```python
import subprocess
import os

# URL de ejemplo — reemplazar con el video deseado
# Sugerencia: usar videos con licencia Creative Commons
VIDEO_URL = "https://www.youtube.com/watch?v=EJEMPLO"

# Directorio de salida
OUTPUT_DIR = "audios"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Descarga solo audio en formato mp3
subprocess.run([
    "yt-dlp",
    "--extract-audio",
    "--audio-format", "mp3",
    "--audio-quality", "0",  # mejor calidad
    "--output", f"{OUTPUT_DIR}/%(title)s.%(ext)s",
    VIDEO_URL
], check=True)

print("Audio descargado exitosamente.")
print("Archivos en el directorio:")
for f in os.listdir(OUTPUT_DIR):
    print(f"  · {f}")
```

---

### CELDA 9 — Markdown: Alternativa — yt-dlp como biblioteca Python
Breve nota: `yt-dlp` también se puede usar como módulo Python importable, sin subprocess. Mostrar la alternativa para que conozcan ambos enfoques.

---

### CELDA 10 — Código: yt-dlp como módulo Python
```python
import yt_dlp

URL = "https://www.youtube.com/watch?v=EJEMPLO"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'audios/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=True)
    print(f"Título: {info['title']}")
    print(f"Duración: {info['duration']} segundos")
    print(f"Canal: {info['uploader']}")
```

---

### CELDA 11 — Markdown: Paso 2 — Transcripción con Whisper
Explicar:
- Whisper es un modelo transformer encoder-decoder entrenado en 680.000 horas de audio multilingüe.
- Tiene varios tamaños de modelo: tiny, base, small, medium, large. A mayor tamaño, mejor calidad pero más lento y más RAM/VRAM.
- Para español, el modelo `small` o `medium` ya da buenos resultados.
- **Recomendación para máquinas sin GPU:** usar modelo `base` o `small`. Con GPU: `medium` o `large`.
- Explicar brevemente que Whisper devuelve: texto completo, segmentos con timestamps, y el idioma detectado.

Incluir una **tabla** con los modelos, tamaño en parámetros, RAM requerida aproximada, y velocidad relativa.

---

### CELDA 12 — Código: Transcripción con Whisper
```python
import whisper

# Cargar modelo — elegir según recursos disponibles:
# "tiny" (~1GB RAM), "base" (~1GB), "small" (~2GB), "medium" (~5GB), "large" (~10GB)
modelo = whisper.load_model("small")

# Ruta al archivo de audio descargado
AUDIO_PATH = "audios/nombre_del_audio.mp3"  # Ajustar según el archivo descargado

# Transcribir
resultado = modelo.transcribe(
    AUDIO_PATH,
    language="es",      # Forzar español (opcional, Whisper detecta automáticamente)
    verbose=True        # Muestra progreso en tiempo real
)

# Texto completo
print("=" * 60)
print("TRANSCRIPCIÓN COMPLETA")
print("=" * 60)
print(resultado["text"])
```

---

### CELDA 13 — Código: Explorar segmentos con timestamps
```python
# Cada segmento tiene: inicio, fin, texto
print(f"Idioma detectado: {resultado['language']}")
print(f"Total de segmentos: {len(resultado['segments'])}")
print()

# Mostrar primeros 10 segmentos
for seg in resultado["segments"][:10]:
    inicio = seg["start"]
    fin = seg["end"]
    texto = seg["text"].strip()
    print(f"[{inicio:07.2f} → {fin:07.2f}] {texto}")
```

---

### CELDA 14 — Markdown: Paso 3 — Exportación y persistencia del corpus
Explicar:
- Una vez transcrito, el texto se guarda como archivo .txt o .json para uso posterior en el pipeline de PLN.
- El formato JSON preserva los timestamps (útil para análisis temporal del discurso).
- El formato TXT plano es lo que va directo a spaCy / text mining.

---

### CELDA 15 — Código: Guardar transcripción en .txt y .json
```python
import json

OUTPUT_DIR = "transcripciones"
os.makedirs(OUTPUT_DIR, exist_ok=True)

nombre_base = os.path.splitext(os.path.basename(AUDIO_PATH))[0]

# Guardar texto plano
txt_path = f"{OUTPUT_DIR}/{nombre_base}.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(resultado["text"])
print(f"Texto plano guardado en: {txt_path}")

# Guardar JSON con segmentos y metadatos
json_path = f"{OUTPUT_DIR}/{nombre_base}.json"
datos = {
    "fuente": VIDEO_URL,
    "idioma_detectado": resultado["language"],
    "texto_completo": resultado["text"],
    "segmentos": [
        {
            "inicio": seg["start"],
            "fin": seg["end"],
            "texto": seg["text"].strip()
        }
        for seg in resultado["segments"]
    ]
}
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
print(f"JSON con segmentos guardado en: {json_path}")
```

---

### CELDA 16 — Markdown: Alternativa liviana — faster-whisper
Breve explicación:
- `faster-whisper` usa CTranslate2, una implementación optimizada que es hasta 4x más rápida y consume menos RAM.
- La API es ligeramente distinta pero el resultado es equivalente.
- Recomendada para máquinas con recursos limitados.

---

### CELDA 17 — Código: Transcripción con faster-whisper
```python
# Alternativa: faster-whisper (más rápido, menos RAM)
# Instalar: pip install faster-whisper

from faster_whisper import WhisperModel

# Modelos: "tiny", "base", "small", "medium", "large-v3"
# compute_type: "int8" para CPU, "float16" para GPU
modelo_fw = WhisperModel("small", device="cpu", compute_type="int8")

segmentos, info = modelo_fw.transcribe(AUDIO_PATH, language="es")

print(f"Idioma detectado: {info.language} (probabilidad: {info.language_probability:.2%})")
print()

texto_completo = []
for seg in segmentos:
    print(f"[{seg.start:07.2f} → {seg.end:07.2f}] {seg.text.strip()}")
    texto_completo.append(seg.text.strip())

transcripcion = " ".join(texto_completo)
print("\n" + "=" * 60)
print(transcripcion)
```

---

### CELDA 18 — Markdown: Pipeline completo — De URL a corpus listo para spaCy
Título: "Integrando todo: función reutilizable"

Explicar que ahora van a encapsular todo el flujo en una función que recibe una URL de YouTube y devuelve texto listo para procesar.

---

### CELDA 19 — Código: Función integradora del pipeline completo
```python
def youtube_a_texto(url: str, modelo_whisper: str = "small",
                     idioma: str = "es", output_dir: str = "corpus") -> dict:
    """
    Pipeline completo: URL de YouTube → audio → transcripción → texto.
    
    Parámetros:
        url: URL del video de YouTube
        modelo_whisper: tamaño del modelo ("tiny", "base", "small", "medium", "large")
        idioma: código de idioma ISO 639-1
        output_dir: directorio de salida para archivos generados
    
    Retorna:
        dict con claves: titulo, duracion, texto, segmentos, archivos_generados
    """
    import yt_dlp
    import whisper
    import json
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Paso 1: Descargar audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info['title']
        duracion = info['duration']
        # Obtener ruta del archivo descargado
        audio_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
    
    print(f"Audio descargado: {titulo} ({duracion}s)")
    
    # Paso 2: Transcribir
    modelo = whisper.load_model(modelo_whisper)
    resultado = modelo.transcribe(audio_path, language=idioma)
    
    print(f"Transcripción completa: {len(resultado['segments'])} segmentos")
    
    # Paso 3: Guardar outputs
    nombre_base = titulo.replace("/", "_").replace("\\", "_")[:80]
    
    txt_path = f"{output_dir}/{nombre_base}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(resultado["text"])
    
    json_path = f"{output_dir}/{nombre_base}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "fuente": url,
            "titulo": titulo,
            "duracion_segundos": duracion,
            "idioma": resultado["language"],
            "texto": resultado["text"],
            "segmentos": [
                {"inicio": s["start"], "fin": s["end"], "texto": s["text"].strip()}
                for s in resultado["segments"]
            ]
        }, f, ensure_ascii=False, indent=2)
    
    return {
        "titulo": titulo,
        "duracion": duracion,
        "texto": resultado["text"],
        "segmentos": resultado["segments"],
        "archivos_generados": [audio_path, txt_path, json_path]
    }

# Uso:
# corpus = youtube_a_texto("https://www.youtube.com/watch?v=EJEMPLO")
# print(corpus["texto"][:500])
```

---

### CELDA 20 — Markdown: Descarga por lotes — Construir un corpus desde una playlist o lista de URLs
Breve explicación de cómo escalar: procesar múltiples videos para construir un corpus más amplio.

---

### CELDA 21 — Código: Procesamiento por lotes
```python
# Lista de URLs a procesar
urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3",
]

resultados = []
errores = []

for i, url in enumerate(urls, 1):
    print(f"\n{'='*60}")
    print(f"Procesando {i}/{len(urls)}: {url}")
    print(f"{'='*60}")
    try:
        r = youtube_a_texto(url, modelo_whisper="small")
        resultados.append(r)
        print(f"OK: {r['titulo']} — {len(r['texto'])} caracteres")
    except Exception as e:
        errores.append({"url": url, "error": str(e)})
        print(f"ERROR: {e}")

print(f"\nResumen: {len(resultados)} exitosos, {len(errores)} errores")

# Corpus completo concatenado
corpus_total = "\n\n---\n\n".join([r["texto"] for r in resultados])
print(f"Corpus total: {len(corpus_total)} caracteres, ~{len(corpus_total.split())} palabras")
```

---

### CELDA 22 — Markdown: Ejercicios propuestos
Título: "Actividades"

Plantear 3 ejercicios con dificultad creciente:

1. **Ejercicio básico:** Elegir un video de YouTube en español (conferencia, entrevista o clase abierta) con licencia Creative Commons. Descargarlo, transcribirlo con Whisper, guardar el resultado en .txt y .json. Reportar: duración del audio, tiempo de transcripción, cantidad de palabras obtenidas, y una evaluación subjetiva de la calidad (¿el texto es legible? ¿hay errores evidentes?).

2. **Ejercicio intermedio:** Comparar la transcripción de Whisper (modelo `small`) con los subtítulos automáticos de YouTube para el mismo video. yt-dlp permite descargar subtítulos con `--write-auto-sub --sub-lang es`. Analizar: ¿qué sistema produce mejor texto? ¿En qué tipo de errores difiere cada uno? ¿Cuál es más útil como input para un pipeline de PLN?

3. **Ejercicio avanzado:** Construir un mini-corpus de al menos 5 videos de un mismo tema o canal. Procesar todos en lote. Calcular estadísticas descriptivas del corpus resultante: total de palabras, promedio por video, vocabulario único, y las 20 palabras más frecuentes (pueden usar `collections.Counter`). Reflexionar: ¿el corpus obtenido sería útil para entrenar o fine-tunear un modelo de lenguaje? ¿Qué preprocesamiento adicional necesitaría?

---

### CELDA 23 — Markdown: Puente hacia la próxima clase
Título: "¿Qué sigue?"

Párrafo de cierre que conecte con spaCy:
- Ya tenemos texto de la web (webscraping) y texto de fuentes audiovisuales (transcripción). El bloque de adquisición de corpus está cerrado.
- El texto transcrito tiene características particulares: ausencia de puntuación precisa, hesitaciones, repeticiones, solapamientos. Eso lo hace un caso interesante para el procesamiento lingüístico.
- En la próxima clase, vamos a tomar estos textos y procesarlos con spaCy: tokenización, lematización, POS tagging, NER. El input será tanto texto scrapeado como texto transcrito, para comparar cómo se comporta el pipeline con cada tipo de fuente.

---

### CELDA 24 — Markdown: Recursos y referencias
- `yt-dlp` documentación: https://github.com/yt-dlp/yt-dlp
- Whisper paper: Radford, A. et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision." OpenAI.
- `faster-whisper`: https://github.com/SYSTRAN/faster-whisper
- `whisperX` (alineación temporal + diarización): https://github.com/m-bain/whisperX
- Consideraciones éticas sobre ASR: Bender, E. M. et al. (2021). "On the Dangers of Stochastic Parrots." — sección sobre datos de entrenamiento y sesgos en modelos de lenguaje.

---

## INSTRUCCIONES TÉCNICAS PARA EL AGENTE

1. **Formato de salida:** Jupyter Notebook (.ipynb) válido. Cada sección marcada arriba como "Markdown" va en una celda Markdown. Cada sección marcada como "Código" va en una celda de código Python.

2. **URLs de ejemplo:** Reemplazar `EJEMPLO`, `VIDEO1`, `VIDEO2`, `VIDEO3` con URLs reales de videos en español con licencia Creative Commons o dominio público. Buscar conferencias académicas, charlas TED en español, o videos del canal de YouTube de universidades públicas argentinas.

3. **Estilo del código:** PEP 8, comentarios en español, docstrings en español. Nombres de variables en español (snake_case). Type hints cuando sea natural.

4. **Estilo del texto:** Aplicar la skill de tono rioplatense académico adjunta. En particular: pretérito perfecto simple, sin emojis, sin expresiones coloquiales informales, lenguaje técnico preciso.

5. **Testeo:** Cada celda de código debe ser ejecutable de forma independiente (asumiendo que las celdas anteriores se ejecutaron). Verificar que los imports estén donde se necesitan.

6. **Extensión:** El notebook completo debería tener entre 24 y 28 celdas. No agregar contenido innecesario, pero tampoco comprimir en exceso. El objetivo es un laboratorio de 2 horas.

7. **NO incluir:** Contenido sobre spaCy ni text mining (eso es la próxima clase). Tampoco incluir fine-tuning de Whisper ni entrenamiento de modelos de ASR.
